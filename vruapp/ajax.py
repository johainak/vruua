from django.http import JsonResponse
import re

from .models import TDR


def get_userAgent(request):
    imsi_id= request.GET.get('imsi')
    userAgent_id = TDR.objects.all()
    options = '<option value="" selected="selected">---------</option>'
    if imsi_id:
        userAgents = TDR.objects.filter(imsi=imsi_id)
    for userAgent in userAgents :
        options += '<option value="%s">%s</option>' % (
            userAgent.userAgent,
            userAgent.userAgent
        )
    response = {}
    response['userAgents'] = options
    return JsonResponse(response)

def get_vulnerabilities(request):
    userAgent_id = request.GET.get('userAgent')
    title = "The Latest Vulnerabilities"
    source = "http://www.cvedetails.com/widget.php?numrows=10&vendor_id=0&product_id=0&version_id=0&hasexp=0&opec=0&opov=0&opcsrf=0&opfileinc=0&opgpriv=0&opsqli=0&opxss=1&opdirt=0&opmemc=0&ophttprs=1&opbyp=0&opginf=0&opdos=0&orderby=3&cvssscoremin=0"
    response ={}
    response['title']='The Latest Vulnerabilities'
    response['widget']= '<iframe src="http://www.cvedetails.com/widget.php?numrows=10&vendor_id=0&product_id=0&version_id=0&hasexp=0&opec=0&opov=0&opcsrf=0&opfileinc=0&opgpriv=0&opsqli=0&opxss=1&opdirt=0&opmemc=0&ophttprs=1&opbyp=0&opginf=0&opdos=0&orderby=3&cvssscoremin=0" width="100%" height="300px"></iframe>'
    versionId='0'
    Name = ''

    if 'Dalvik' in userAgent_id :
        elementVersion = re.findall('Android [0-9]\.[0-9]\.[0-9]', userAgent_id)
        versionNumber=elementVersion[0].split(' ')
        vendorId='1224'
        productId='19997'
        Name = elementVersion[0]
        if versionNumber[1] == '8.0.0':
            versionId='223494'

        elif versionNumber[1] == '6.0.1':
            versionId ='188440'
            print versionNumber
        elif versionNumber[1] == '4.4.4':
            versionId= '177951'
            print versionNumber
        else:
            versionId= '0'

    elif 'Mozilla' in userAgent_id:
        if 'OPR/' in userAgent_id:
            elementVersion=re.findall('OPR\/[0-9]{2}\.[0-9]\.[0-9]{4}', userAgent_id)
            elementVersion[0]=elementVersion[0].replace ('OPR/','Opera ')
            vendorId = '1961'
            productId = '15008'
            Name='Opera'
        elif 'Chrome' in userAgent_id :
            elementVersion=re.findall('Chrome\/[0-9]{2}\.[0-9]\.[0-9]{4}\.[0-9]{2}', userAgent_id)
            elementVersion[0]=elementVersion[0].replace ('/',' ')
            vendorId = '1224'
            productId = '19997'
            Name = 'Chrome'
        elif 'Firefox' in userAgent_id:
            elementVersion = re.findall('Firefox\/[0-9]{2}\.[0-9]', userAgent_id)
            elementVersion[0] = elementVersion[0].replace('\/',' ')
            vendorId = '452'
            productId = '3264'
            Name = 'Firefox'
        elif 'Version' in userAgent_id and 'Safari'in userAgent_id:
            elementVersion = re.findall('Version\/[0-9]{2}\.[0-9]', userAgent_id)
            elementVersion[0]=elementVersion[0].replace('Version','Safari')
            elementVersion[0] = elementVersion[0].replace ('/',' ')
            vendorId = '49'
            productId = '2935'
            Name = 'Safari'

    elif 'Cronet' in userAgent_id:
        elementVersion = 'a google app no included in the analysis'
    elif 'Chrome' in userAgent_id :
        elementVersion = re.findall('Chrome\/[0-9]{2}\.[0-9]\.[0-9]{4}\.[0-9]{2}', userAgent_id)
        elementVersion[0] = elementVersion[0].replace('/', ' ')

        vendorId = '1224'
        productId = '19997'
    elif 'iOS/' in userAgent_id:
        elementVersion = re.findall('iOS\/[0-9]{2}\.[0-9]\.[0-9]' , userAgent_id)
        elementVersion[0]=elementVersion[0].replace('/', ' ')
        vendorId = '49'
        productId = '15556'
    else:
        elementVersion='unknown app or OS'


    if Name != '':
        response['element'] = '<h4>This User-Agent is from <strong>' + elementVersion[0] + '</strong> </h4>'
        response['vulDescription']='<h4>The latest vulnerabilities found for ' + Name + ' <i>(Source CVE details)</i></h4>'
        response['widget'] = '<iframe style="border:none" src="http://www.cvedetails.com/widget.php?numrows=10&vendor_id=' + vendorId + '&product_id=' + productId + '&version_id=' + versionId + '" width="100%" height="300px"></iframe>'
    else:
        response['element'] = '<h4>This User-Agent is from <strong>' + elementVersion + '</strong> </h4>'
        response['vulDescription'] ='<h>No vulnerabilities found</h4>'
        response['widget'] ='<h4>Try another User-agent</h4>'
    return JsonResponse(response)

