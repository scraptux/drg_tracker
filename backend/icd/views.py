from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Q

from .models import Version, Kapitel, Gruppen, Kodes, Umsteiger

@api_view(['GET'])
def version(request):
    year = request.query_params.get('year')
    if year: return Response(int(year))
    return Response(get_version())

def get_version():
    res = []
    for r in Version.objects.all():
        res.append(r.Year)
    return res


@api_view(['GET'])
def kapitel(request):
    year = int(request.query_params.get('year'))
    if not year:
        return HttpResponseBadRequest("please specify the year parameter")
    kapnr = request.query_params.get('kapnr')
    kapid = request.query_params.get('kapid')
    return Response({
        'year': year,
        'kapitel': get_kapitel(year, kapnr, kapid)
    })

def get_kapitel(year = None, kapnr = None, kapid = None):
    res = []
    r = Kapitel.objects.all()
    if year: r = r.filter(Year=Version.objects.get(Year=year))
    if kapnr: r = r.filter(KapNr=kapnr)
    if kapid: r = r.filter(id=kapid)
    for x in r:
        res.append({
            'KapNr': x.KapNr,
            'KapTi': x.KapTi,
            'Year': x.Year.Year
        })
    return res


@api_view(['GET'])
def gruppen(request):
    year = int(request.query_params.get('year'))
    if not year:
        return HttpResponseBadRequest("please specify the year parameter")
    kapitel = request.query_params.get('kapitel')
    grvon = request.query_params.get('grvon')
    return Response({
        'year': year,
        'kapitel': get_kapitel(year, kapitel, None),
        'gruppen': get_gruppen(year, kapitel, grvon)
    })

def get_gruppen(year = None, kapitel = None, grvon = None):
    res = []
    r = Gruppen.objects.all()
    if year:
        y = Version.objects.get(Year=year)
        r = r.filter(Year=y)
        if kapitel: r = r.filter(KapNr=Kapitel.objects.get(KapNr=kapitel, Year=y))
        elif grvon: r = r.filter(GrVon=grvon)
    for x in r:
        res.append({
            'GrVon': x.GrVon,
            'GrBis': x.GrBis,
            'KapNr': x.KapNr.KapNr,
            'GrTi': x.GrTi,
            'Year': x.Year.Year
        })
    return res


@api_view(['GET'])
def kodes(request):
    year = int(request.query_params.get('year'))
    if not year:
        return HttpResponseBadRequest("please specify the year parameter")
    grvon = request.query_params.get('grvon')
    codestart = request.query_params.get('codestart')
    codeexact = request.query_params.get('codeexact')
    
    kodes_exact = get_kodes(year, grvon, None, codeexact)
    kodes_start = None
    if codestart:
        kodes_start = get_kodes(year, None, codestart, None)
    
    if len(kodes_exact) == 0:
        return HttpResponseBadRequest("code not found")
    kapitel = get_kapitel(year, kodes_exact[0]['KapNr'], None)
    gruppe = get_gruppen(year, None, kodes_exact[0]['GrVon'])
    return Response({
        'year': year,
        'kapitel': kapitel,
        'gruppe': gruppe,
        'kodes': kodes_exact,
        'kodes_start': kodes_start
    })

def get_kodes(year = None, grvon = None, codestart = None, codeexact = None):
    res = []
    r = Kodes.objects.all()
    if year:
        y = Version.objects.get(Year=year)
        r = r.filter(Year=y)
        if grvon: r = r.filter(GrVon=Gruppen.objects.get(GrVon=grvon, Year=y), Ebene=3)
        elif codestart: r = r.filter(CodeOhnePunkt__startswith=codestart, Ebene__gt=3)
        elif codeexact: r = r.filter(CodeOhnePunkt__exact=codeexact)
    for x in r:
        res.append({
            'KapNr': x.KapNr.KapNr,
            'GrVon': x.GrVon.GrVon,
            'Code': x.Code,
            'NormCode': x.NormCode,
            'CodeOhnePunkt': x.CodeOhnePunkt,
            'Titel': x.Titel,
            'Dreisteller': x.Dreisteller,
            'Viersteller': x.Viersteller,
            'Fünfsteller': x.Fünfsteller,
            'Year': x.Year.Year
        })
    return res


@api_view(['GET'])
def track(request):
    # get params
    year_start = request.query_params.get('year_start')
    year_stop = request.query_params.get('year_stop')
    year_param = request.query_params.get('year')
    code_param = request.query_params.get('code')
    if not year_start or not year_stop or not code_param:
        return HttpResponseBadRequest("missing parameters")
    year_start = int(year_start)
    year_stop = int(year_stop)
    if not year_param:
        year_param = year_stop
    return get_track(year_start, year_stop, code_param, year_param)

def get_track(year_start, year_stop, code_param, year_param):
    problem_code = 0
    tmp_nodes = []
    tmp_links = []

    for year in range(year_start, year_stop+1):
        year_object = Version.objects.get(Year=year)
        codes = Kodes.objects.filter(CodeOhnePunkt__startswith=code_param, Year=year_object)
        if codes.count() == 0:  # no code in that year
            problem_code = max(problem_code, 3)
            continue
        for code in codes:
            if code.Code[-1] == '-':
                continue
            if code.Old.count() == 0 and code.New.count() == 0:  # not in list and would be added without links
                continue 
            if code in tmp_nodes:
                continue
            tmp_nodes.append(code)
            problem_code = max(problem_code, traverseUmsteiger(code, -1, tmp_nodes, tmp_links, year_start, year_stop, code_param))
            problem_code = max(problem_code, traverseUmsteiger(code, 1, tmp_nodes, tmp_links, year_start, year_stop, code_param))

    # create axis
    codes_list = list(set([node.Code for node in tmp_nodes]))
    codes_list.sort()
    years_list = [y for y in range(year_start, year_stop+1)]
    years_list.sort()

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
        nodes.append({
            'x': x[node.Code],
            'y': y[node.Year.Year],
            'text': node.Code,
            'drg': 'ops',
            'year': node.Year.Year,
            'title': node.Titel
        })
    links = []
    for link in tmp_links:
        links.append({
            'source': {'x': x[link[0].Code], 'y': y[link[0].Year.Year]}, 
            'target': {'x': x[link[1].Code], 'y': y[link[1].Year.Year]}
        })

    # return results
    years = [{'y': y, 'text': text} for text, y in y.items()]
    year_object = Version.objects.get(Year=year_param)
    group = Kodes.objects.get(CodeOhnePunkt__exact=code_param, Year=year_object)
    groupcode = Kodes.objects.get(CodeOhnePunkt__exact=code_param[0:3], Year=year_object)
    res = {
        'nodes': nodes,
        'links': links,
        'years': years,
        'code_count': len(x),
        'code_list': codes_list,
        'status_code': problem_code,
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

def traverseUmsteiger(code, step, tmp_nodes, tmp_links, year_start, year_stop, code_param):
    problem_code = 0
    codes = []
    if step == -1 and code.Year.Year > year_start:
        codes = code.New.all()
    elif step == 1 and code.Year.Year < year_stop:
        codes = code.Old.all()
    for c in codes:
        linked_kode = c.Old if step == -1 else c.New
        # check for problems
        if linked_kode in tmp_nodes:  # code already in linked
            continue
        if not linked_kode:
            continue
        tmp_nodes.append(linked_kode)
        tmp_links.append([code, linked_kode])
        if not linked_kode:  # loose node
            problem_code = max(problem_code, 2)
            continue
        if code.CodeOhnePunkt != linked_kode.CodeOhnePunkt:  # non straight connection found
            problem_code = max(problem_code, 1)
        if code_param not in linked_kode.CodeOhnePunkt:  # code not included in search query
            problem_code = max(problem_code, 2)
        p = traverseUmsteiger(linked_kode, -1, tmp_nodes, tmp_links, year_start, year_stop, code_param)
        problem_code = max(problem_code, p)
        p = traverseUmsteiger(linked_kode, 1, tmp_nodes, tmp_links, year_start, year_stop, code_param)
        problem_code = max(problem_code, p)
        
    return problem_code


@api_view(['GET'])
def search(request):
    # get params
    s = request.query_params.get('s')
    year = request.query_params.get('year')
    if not s:
        return HttpResponseBadRequest("no search query specified")
    if not year:
        year = 2024
    else:
        year = int(year)
    # set year
    kodes = Kodes.objects.filter(Year=Version.objects.get(Year=year))
    # filter for code
    res = []
    searchResponseJSON(kodes.filter(Q(Code__icontains=s) | Q(CodeOhnePunkt__icontains=s)), res)
    # filter for text
    for splice in s.split(' '):
        kodes = kodes.filter(Titel__icontains=splice)
    searchResponseJSON(kodes, res)
    # return
    return Response(res)

def searchResponseJSON(kodes_list, res):
    for kode in kodes_list:
        res.append({
            'Titel': kode.Titel,
            'Code': kode.Code,
            'CodeOhnePunkt': kode.CodeOhnePunkt,
            'Year': kode.Year.Year
        })