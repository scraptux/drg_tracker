from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.core import serializers
from django.http import JsonResponse
from django.db.models import Q

from .models import Version, Kapitel, Gruppen, Kodes, Umsteiger
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
        grvon = req.query_params.get('grvon')
        codestart = req.query_params.get('codestart')
        codeexact = req.query_params.get('codeexact')
        if year:
            y = Version.objects.get(Year=year)
            self.queryset = self.queryset.filter(Year=y)
            if grvon:
                gr = Gruppen.objects.get(GrVon=grvon, Year=y)
                self.queryset = self.queryset.filter(GrVon=gr, Ebene=3)
                return self.queryset
            elif codestart:
                self.queryset = self.queryset.filter(CodeOhnePunkt__startswith=codestart, Ebene__gt=3)
                return self.queryset
            elif codeexact:
                self.queryset = self.queryset.filter(CodeOhnePunkt__exact=codeexact)
                return self.queryset

@api_view()
def track(request):
    year = request.query_params.get('year')
    overview = request.query_params.get('overview')
    get_nodes = request.query_params.get('get_nodes')
    if not year:
        year_start = int(request.query_params.get('year_start'))
        year = year_stop = int(request.query_params.get('year_stop'))
    else:
        year_start = request.query_params.get('year_start')
        year_stop = request.query_params.get('year_stop')
        if year_start and year_stop:
            year_start = int(year_start)
            year_stop = int(year_stop)
            if int(year) < year_start:
                year = str(year_start)
            elif int(year) > year_stop:
                year = str(year_stop)
        else:
            years = Version.objects.order_by('Year')
            year_start = years.first().Year
            year_stop = years.last().Year
    if overview:
        complete_results = False
    else:
        complete_results = True
    if get_nodes:
        only_nodes = True
    else:
        only_nodes = False
    
    code = request.query_params.get('code')
    year_object = Version.objects.get(Year=year)
    group = Kodes.objects.get(CodeOhnePunkt__exact=code, Year=year_object)
    tracking = []
    subcodes = Kodes.objects.filter(CodeOhnePunkt__startswith=code, Year=year_object)
    if subcodes.count() != 1:
        for kode in subcodes:
            if not Umsteiger.objects.filter(Q(Old=kode) | Q(New=kode)):
                continue
            tracking.append(kode)
    else:
        tracking= [Kodes.objects.get(CodeOhnePunkt__exact=code, Year=year_object)]

    checked = []
    checked.extend(tracking)
    nodes = []
    links = []
    for code in tracking:
        tmp_nodes, tmp_links = trackPaths(code, checked, year_start, year_stop)
        nodes.extend(tmp_nodes)
        nodes.extend([{"x": code.Code, "y": code.Year.Year, "text": code.Code}])
        links.extend(tmp_links)
    
    codes_list = []
    years_list = []
    for node in nodes:
        if node["x"] not in codes_list:
            codes_list.append(node["x"])
        #if node["y"] not in years_list:
            #years_list.append(node["y"])
    for year in range(year_start, year_stop+1):
        #print(year)
        years_list.append(year)
    codes_list.sort()
    years_list.sort()

    if only_nodes:
        res = []
        for c in codes_list:
            res.append({'Code': c})
        return Response(codes_list)

    x = {}
    for idx, code in enumerate(codes_list):
        x[code] = idx
    y = {}
    for idx, key in enumerate(years_list):
        y[key] = idx
    
    # nodes = [{'x': code.Code, 'y': code.Year.Year, 'text': code.Code}, ...]
    # becomes
    # nodes = [{'x': code-coords, 'y': year-coords, 'text': code.Code}, ...]
    for node in nodes:
        node['x'] = x[node['x']]
        node['y'] = y[node['y']]
    # links = [{'source': {'x': code.Code, 'y': code.Year.Year}, 'target': {'x': new.Code, 'y': new.Year.Year}}, ...]
    # becomes
    # links = [{'source': {'x': code-coords, 'y': year-coords}, 'target': {'x': newcode-coords, 'y': newyear-coords}}, ...]
    for link in links:
        link['source']['x'] = x[link['source']['x']]
        link['source']['y'] = y[link['source']['y']]
        link['target']['x'] = x[link['target']['x']]
        link['target']['y'] = y[link['target']['y']]
    
    if not complete_results:
        # check for problem
        problem_code = 0
        # problem might exist if: split/merged                       ! or new/deleted code (not checked)
        nodes_to_examine = []
        for link in links:
            if link['source']['x'] != link['target']['x']:
                problem_code = 1
                nodes_to_examine.append(link['source']['x'])
        # problem exists if: code changed
        nodes_examined = {} # counts how many connections to the same code exist (should be year-count)
        """for link in links:
            if link['source']['x'] not in nodes_to_examine:
                continue
            if link['source']['x'] not in nodes_examined:
                nodes_examined[link['source']['x']] = 0
            if link['source']['x'] == link['target']['x']:
                nodes_examined[link['source']['x']] += 1
        for node in nodes_examined:
            if nodes_examined[node] != (len(y)-1)*2 and node == code:
                problem_code = 2
                break"""
        for link in links:
            if link['source']['x'] in nodes_to_examine:
                if link['source']['x'] not in nodes_examined:
                    nodes_examined[link['source']['x']] = {}
                if link['source']['y'] not in nodes_examined[link['source']['x']]:
                    nodes_examined[link['source']['x']][link['source']['y']] = 0
                nodes_examined[link['source']['x']][link['source']['y']] += 1
            if link['target']['x'] in nodes_to_examine:
                if link['target']['x'] not in nodes_examined:
                    nodes_examined[link['target']['x']] = {}
                if link['target']['y'] not in nodes_examined[link['target']['x']]:
                    nodes_examined[link['target']['x']][link['target']['y']] = 0
                nodes_examined[link['target']['x']][link['target']['y']] += 1
        for node in nodes_examined:
            #for idx, year in enumerate(y):
            for year in nodes_examined[node]:
                if year == 0 or year == len(y)-1:
                    if nodes_examined[node][year] < 2:
                        problem_code = 2
                        break
                else:
                    if nodes_examined[node][year] < 4:
                        problem_code = 2
                        break
            if problem_code == 2:
                break
        # if problem return error message and code
        groupcode = Kodes.objects.get(CodeOhnePunkt__exact=code[0:3], Year=group.Year)
        res = {
            'status_code': problem_code,
            #'code': group
            'code': {'KapNr': group.KapNr.KapNr,
                     'KapTi': group.KapNr.KapTi,
                     'GrVon': group.GrVon.GrVon,
                     'GrBis': group.GrVon.GrBis,
                     'GrTi': group.GrVon.GrTi,
                     'GruppeCode': groupcode.Code,
                     'GruppeCodeNorm': groupcode.CodeOhnePunkt,
                     'Code': group.Code,
                     'NormCode': group.NormCode,
                     'CodeOhnePunkt': group.CodeOhnePunkt,
                     'Titel': group.Titel,
                     'Year': group.Year.Year}
        }
        return Response(res)

    years = [{'y': y, 'text': text} for text, y in y.items()]
    res = {
        'nodes': nodes,
        'links': links,
        'years': years,
        'code_count': len(x)
    }
    return Response(res)

def trackPaths(code, checked_codes, start, stop):
    nodes = []
    links = []
    if code.Year.Year < stop:
        for umstieg in Umsteiger.objects.filter(Old=code):
            new = umstieg.New
            if new is None:
                continue
            links.append({"source": {"x": code.Code, "y": code.Year.Year}, "target": {"x": new.Code, "y": new.Year.Year}})
            if new in checked_codes:
                continue
            nodes.append({"x": new.Code, "y": new.Year.Year, "text": new.Code})
            checked_codes.append(new)
            nnodes, nlinks = trackPaths(new, checked_codes, start, stop)
            nodes.extend(nnodes)
            links.extend(nlinks)
    if code.Year.Year > start:
        for umstieg in Umsteiger.objects.filter(New=code):
            old = umstieg.Old
            if old is None:
                continue
            links.append({"source": {"x": old.Code, "y": old.Year.Year}, "target": {"x": code.Code, "y": code.Year.Year}})
            if old in checked_codes:
                continue
            nodes.append({"x": old.Code, "y": old.Year.Year, "text": old.Code})
            checked_codes.append(old)
            nnodes, nlinks = trackPaths(old, checked_codes, start, stop)
            nodes.extend(nnodes)
            links.extend(nlinks)
    return nodes, links


@api_view()
def search(request):
    s = request.query_params.get('s')
    year = request.query_params.get('year')
    if year:
        kodes = Kodes.objects.filter(Year=Version.objects.get(Year=year)).filter(Q(Code__icontains=s) | Q(CodeOhnePunkt__icontains=s) | Q(Titel__icontains=s))
    else:
        kodes = Kodes.objects.filter(Year=Version.objects.get(Year=2023)).filter(Q(Code__icontains=s) | Q(CodeOhnePunkt__icontains=s) | Q(Titel__icontains=s))
    res = []
    for kode in kodes:
        res.append({
            'Titel': kode.Titel,
            'Code': kode.Code,
            'CodeOhnePunkt': kode.CodeOhnePunkt,
            'Year': kode.Year.Year
        })
    return Response(res)