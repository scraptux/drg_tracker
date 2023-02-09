from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import JsonResponse
from django.db.models import Q

from .models import Version, Kapitel, Gruppen, Kodes, Umsteiger, Dreisteller
from .serializers import VersionSerializer, KapitelSerializer, GruppenSerializer, KodesSerializer


class YearsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

class KapitelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Kapitel.objects.all()
    serializer_class = KapitelSerializer

    def get_queryset(self):
        req = self.request
        year = req.query_params.get('year')
        kapnr = req.query_params.get('kapnr')
        kapid = req.query_params.get('kapid')
        if year:
            self.queryset = self.queryset.filter(Year=Version.objects.get(Year=year))
        if kapnr:
            self.queryset = self.queryset.filter(KapNr=kapnr)
        if kapid:
            self.queryset = self.queryset.filter(id=kapid)
        return self.queryset

class GruppenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Gruppen.objects.all()
    serializer_class = GruppenSerializer

    def get_queryset(self):
        req = self.request
        year = req.query_params.get('year')
        kapitel = req.query_params.get('kapitel')
        grvon = req.query_params.get('grvon')
        grid = req.query_params.get('grid')
        if year:
            y = Version.objects.get(Year=year)
            self.queryset = self.queryset.filter(Year=y)
            if kapitel:
                kap = Kapitel.objects.get(KapNr=kapitel, Year=y)
                self.queryset = self.queryset.filter(KapNr=kap)
                return self.queryset
            elif grvon:
                self.queryset = self.queryset.filter(GrVon=grvon)
                return self.queryset
            elif grid:
                self.queryset = self.queryset.filter(id=grid)
                return self.queryset

class KodesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Kodes.objects.all()
    serializer_class = KodesSerializer

    def get_queryset(self):
        req = self.request
        year = req.query_params.get('year')
        dcode = req.query_params.get('dcode')
        codestart = req.query_params.get('codestart')
        codeexact = req.query_params.get('codeexact')
        if year:
            y = Version.objects.get(Year=year)
            self.queryset = self.queryset.filter(Year=y)
            if dcode:
                dc = Dreisteller.objects.get(DCode=dcode, Year=y)
                self.queryset = self.queryset.filter(DCode=dc, Ebene=4)
                return self.queryset
            elif codestart:
                self.queryset = self.queryset.filter(Code__startswith=codestart, Ebene__gt=4)
                return self.queryset
            elif codeexact:
                self.queryset = self.queryset.filter(Code__exact=codeexact)
                return self.queryset

@api_view(['GET'])
def get_dreisteller(request):
    year = request.query_params.get('year')
    grvon = request.query_params.get('grvon')
    did = request.query_params.get('did')

    y = Version.objects.get(Year=year)
    if grvon:
        group = Gruppen.objects.get(GrVon=grvon, Year=y)
        codes = Dreisteller.objects.filter(GrVon=group, Year=y).order_by('DCode')
        context = [{'KapNr': code.KapNr.id, 'GrVon': code.GrVon.id, 'DCode': code.DCode, 'DTi': code.DTi} for code in codes]
        return Response(context)
    elif did:
        dcode = Dreisteller.objects.get(id=did)
        context = [{
            'DCode': dcode.DCode,
            'DTi': dcode.DTi
        }]
        return Response(context)
    return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

@api_view()
def track(request):
    # get params
    year_start = request.query_params.get('year_start')
    year_stop = request.query_params.get('year_stop')
    year_param = request.query_params.get('year')
    code_param = request.query_params.get('code')
    if not year_start or not year_stop or not year_param or not code_param:
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)
    year_start = int(year_start)
    year_stop = int(year_stop)
    year_param = int(year_param)
    if year_param < year_start:
        year_param = year_start
    elif year_param > year_stop:
        year_param = year_stop

    # track codes
    problem_code = 0  # 0:green, 1:yellow, 2:orange, 3:red
    tmp_nodes = []
    tmp_links = []
    for year in range(year_start, year_stop+1):
        year_object = Version.objects.get(Year=year)
        subcodes = Kodes.objects.filter(Code__startswith=code_param, Year=year_object)
        if subcodes.count() == 0:  # no code in that year
            problem_code = 3
            continue
        for kode in subcodes:
            if not Umsteiger.objects.filter(Q(Old=kode) | Q(New=kode)):  # not in list and would be added without links
                continue
            tmp_nodes.append(kode)
            if kode.Year.Year > year_start:
                problem_code2 = trackFromUmsteiger(kode, Umsteiger.objects.filter(New=kode), -1, tmp_nodes, tmp_links, year_start, year_stop, code_param)
                if problem_code < problem_code2:
                    problem_code = problem_code2
            if kode.Year.Year < year_stop:
                problem_code2 = trackFromUmsteiger(kode, Umsteiger.objects.filter(Old=kode), 1, tmp_nodes, tmp_links, year_start, year_stop, code_param)
                if problem_code < problem_code2:
                    problem_code = problem_code2

    # create axis
    codes_list = []
    for node in tmp_nodes:
        if node.Code in codes_list:
            continue
        codes_list.append(node.Code)
    codes_list.sort()
    years_list = []
    for year in range(year_start, year_stop+1):
        years_list.append(year)
    years_list.sort()

    # TODO: add to normal return
    if request.query_params.get('get_nodes'):
        res = []
        for c in codes_list:
            res.append({'Code': c})
        return Response(codes_list)

    # create coordinates
    x = {}
    for idx, code in enumerate(codes_list):
        x[code] = idx
    y = {}
    for idx, key in enumerate(years_list):
        y[key] = idx
    
    # create nodes and links
    nodes = []
    for node in tmp_nodes:
        nodes.append({'x': x[node.Code], 'y': y[node.Year.Year], 'text': node.Code})
    links = []
    for link in tmp_links:
        links.append({
            'source': {'x': x[link[0].Code], 'y': y[link[0].Year.Year]}, 
            'target': {'x': x[link[1].Code], 'y': y[link[1].Year.Year]}
        })
        
    # return results
    years = [{'y': y, 'text': text} for text, y in y.items()]
    year_object = Version.objects.get(Year=year_param)
    group = Kodes.objects.get(Code__exact=code_param, Year=year_object)
    groupcode = Kodes.objects.get(Code__exact=code_param[0:5], Year=year_object)
    res = {
        'nodes': nodes,
        'links': links,
        'years': years,
        'code_count': len(x),
        'status_code': problem_code,
        'code': {'KapNr': group.KapNr.KapNr,
                 'KapTi': group.KapNr.KapTi,
                 'GrVon': group.GrVon.GrVon,
                 'GrBis': group.GrVon.GrBis,
                 'GrTi': group.GrVon.GrTi,
                 'DCode': group.DCode.DCode,
                 'DTi': group.DCode.DTi,
                 'GruppeCode': groupcode.Code,
                 'GruppeCodeNorm': groupcode.Code,
                 'Code': group.Code,
                 'Titel': group.Titel,
                 'Year': group.Year.Year}
    }
    return Response(res)

def trackFromUmsteiger(kode, umsteiger, step, tmp_nodes, tmp_links, year_start, year_stop, code_param):
    problem_code = 0
    non_straight_line_found = False
    for umstieg in umsteiger:  # check previous year
        linked_kode = umstieg.Old if step == -1 else umstieg.New
        if not linked_kode:  # loose node
            if problem_code < 2:
                problem_code = 2
            continue
        if linked_kode in tmp_nodes:  # code already in linked
            continue
        if not non_straight_line_found and linked_kode.Code != kode.Code:  # non straight connection found
            non_straight_line_found = True
        if code_param not in linked_kode.Code:  # code not included in search query
            if problem_code < 2:
                problem_code = 2
            trackOutliers(linked_kode, kode, tmp_nodes, tmp_links, year_start, year_stop)
        tmp_links.append([kode, linked_kode])
    if non_straight_line_found:  # non straight connections found
        if problem_code < 1:
            problem_code = 1
    return problem_code

def trackOutliers(kode, tracked_kode, tmp_nodes, tmp_links, year_start, year_stop):
    tmp_nodes.append(kode)
    if kode.Year.Year > year_start:
        trackOutliersFromUmsteiger(kode, tracked_kode, Umsteiger.objects.filter(New=kode), -1, tmp_nodes, tmp_links, year_start, year_stop)
    if kode.Year.Year < year_stop:
        trackOutliersFromUmsteiger(kode, tracked_kode, Umsteiger.objects.filter(Old=kode), 1, tmp_nodes, tmp_links, year_start, year_stop)

def trackOutliersFromUmsteiger(kode, tracked_kode, umsteiger, step, tmp_nodes, tmp_links, year_start, year_stop):
    for umstieg in umsteiger:
        linked_kode = umstieg.Old if step == -1 else umstieg.New
        if linked_kode == tracked_kode:  # do not traverse backwards
            continue
        tmp_links.append([kode, linked_kode])
        trackOutliers(linked_kode, kode, tmp_nodes, tmp_links, year_start, year_stop)

@api_view()
def search(request):
    s = request.query_params.get('s')
    year = request.query_params.get('year')
    if year:
        kodes = Kodes.objects.filter(Year=Version.objects.get(Year=year)).filter(Q(Code__icontains=s) | Q(Titel__icontains=s))
    else:
        kodes = Kodes.objects.filter(Year=Version.objects.get(Year=2023)).filter(Q(Code__icontains=s) | Q(Titel__icontains=s))
    res = []
    for kode in kodes:
        res.append({
            'Titel': kode.Titel,
            'Code': kode.Code,
            'Year': kode.Year.Year
        })
    s = s[0]+"-"+s[1:]
    if year:
        kodes = Kodes.objects.filter(Year=Version.objects.get(Year=year)).filter(Q(Code__icontains=s) | Q(Titel__icontains=s))
    else:
        kodes = Kodes.objects.filter(Year=Version.objects.get(Year=2023)).filter(Q(Code__icontains=s) | Q(Titel__icontains=s))
    for kode in kodes:
        res.append({
            'Titel': kode.Titel,
            'Code': kode.Code,
            'Year': kode.Year.Year
        })
    return Response(res)