#------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Download Tools
# Based on the code from VideoMonkey XBMC Plugin
#------------------------------------------------------------
# pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# Creado por:
# Jesús (tvalacarta@gmail.com)
# jurrabi (jurrabi@gmail.com)
# bandavi (xbandavix@gmail.com)
# Licencia: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
# Historial de cambios:
#------------------------------------------------------------

import urlparse,urllib2,urllib
import time
import os
import config
import logger
import re
import socket
import cookielib

# True - Muestra las cabeceras HTTP en el log
# False - No las muestra
DEBUG_LEVEL = False

CACHE_PATH = config.get_setting("cache.dir")

DEBUG = config.get_setting("debug")

##################################
#         SECCION HTTP           #
##################################

#Funciones Antiguas redirigidas a la funcion downloadpage:
#Se podrán eliminar cuando ningun canal ni server las use.
def downloadpageGzip(url):
  return downloadpage(url,addheaders=[['Accept-Encoding','gzip,deflate']])

def getLocationHeaderFromResponse(url):
  return downloadpage(url,getheaders=True,follow_redirects=False,header_to_get="location", getdata=False)

def get_header_from_response(url,header_to_get="",post=None,headers=None):
  if header_to_get =="location":
    return downloadpage(url,post,headers,getheaders=True,follow_redirects=False, header_to_get=header_to_get, getdata=False)
  else:
    return downloadpage(url,post,headers,getheaders=True,header_to_get=header_to_get, getdata=False)

def get_headers_from_response(url,post=None,headers=None):
  return downloadpage(url,post,headers,getheaders=True, getdata=False)

def read_body_and_headers(url, post=None, headers=None, follow_redirects=False, timeout=None):
  return downloadpage(url,post,headers,follow_redirects,timeout,getheaders=True)

def downloadpageWithoutCookies(url):
  return cache_page(url, cookies=False)

def downloadpageWithCookies(url):
  return cache_page(url)
  
def cachePage(url,post=None,headers=None,follow_redirects=True, timeout=None, cookies=True,addheaders=None):
    return cache_page(url,post,headers,follow_redirects,timeout,cookies=cookies,addheaders=addheaders )



#Descargar páginas con cache (solo contenido no headers)    
def cache_page(url,post=None,headers=None,follow_redirects=True, timeout=None, cookies=True,addheaders=None):
    logger.info("----------------------------------------------")
    logger.info("[scrapertools.py] - cachePage")
    logger.info("----------------------------------------------")
    modoCache = config.get_setting("cache.mode")
    if post is None:
      if modoCache =="0":
        logger.info("Modo Cache: Automatico")
      elif modoCache =="1":
        logger.info("Modo Cache: Cachear todo")
      elif modoCache =="2":
        logger.info("Modo Cache: No Cachear")
    else:
      logger.info("Modo Cache: No Cachear (Petición POST)")

    if modoCache == "2" or post is not None:
      data = downloadpage(url,post,headers, timeout=timeout)
    
    elif modoCache == "1":
        # Obtiene los handlers del fichero en la cache
        cachedFile, newFile = getCacheFileNames(url)
    
        # Si no hay ninguno, descarga
        if cachedFile == "":
            logger.debug("La pagina no está en cache")
    
            # Lo descarga
            data = downloadpage(url,post,headers,follow_redirects, timeout, cookies=cookies,addheaders=addheaders)
            if data:
              # Lo graba en cache
              outfile = open(newFile,"w")
              outfile.write(data)
              outfile.flush()
              outfile.close()
              logger.info("Grabando cache en: " + newFile)
        else:
            logger.info("Leyendo cache de: " + cachedFile)
            infile = open( cachedFile )
            data = infile.read()
            infile.close()
    
    # CACHE_ACTIVA: Descarga de la cache si no ha cambiado
    else:    
        # Datos descargados
        data = ""
        
        # Obtiene los handlers del fichero en la cache
        cachedFile, newFile = getCacheFileNames(url)
    
        # Si no hay ninguno, descarga
        if cachedFile == "":
            logger.debug("La pagina no está en cache")
    
            # Lo descarga
            data = downloadpage(url,post,headers,follow_redirects, timeout, cookies=cookies,addheaders=addheaders)
            if data:
              # Lo graba en cache
              outfile = open(newFile,"w")
              outfile.write(data)
              outfile.flush()
              outfile.close()
              logger.debug("Grabando cache en: " + newFile)
    
        # Si sólo hay uno comprueba el timestamp (hace una petición if-modified-since)
        else:
            # Extrae el timestamp antiguo del nombre del fichero
            oldtimestamp = time.mktime( time.strptime(cachedFile[-20:-6], "%Y%m%d%H%M%S") )
            fechaFormateada = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(oldtimestamp))
            logger.debug("Fecha del Cache: " + fechaFormateada)
            
            # Hace la petición
            headerstoadd = []
            if addheaders is not None:
              headerstoadd.append(addheaders)
            headerstoadd.append(['If-Modified-Since',fechaFormateada])
            data = downloadpage(url,post,headers,follow_redirects, timeout, cookies=cookies,addheaders=headerstoadd)
            # Si ha cambiado
            if data:
                logger.debug("Pagina descargada")
                # Borra el viejo
                logger.debug("Borrando Cache antiguo: "+cachedFile)
                os.remove(cachedFile)
                
                # Graba en cache el nuevo
                outfile = open(newFile,"w")
                outfile.write(data)
                outfile.flush()
                outfile.close()
                logger.info("Grabando cache en: " + newFile)
            # Devuelve el contenido del fichero de la cache
            else:
                logger.debug("Pagina no descargada")
                logger.debug("Leyendo cache de: " + cachedFile)
                infile = open( cachedFile )
                data = infile.read()
                infile.close()

    return data


#Funcion download page, puede descargar la pagina, headers + pagina, headers, o un unico header, segun los parametros pasados:
def downloadpage(url,post=None,headers=None,follow_redirects=True, timeout=None, getheaders=False, header_to_get=None, cookies=True,getdata=True,addheaders=None):

    if header_to_get is not None and getheaders == False:
      getheaders =  True
      getdata = False
      
    url = urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
    dominio = urlparse.urlparse(url)[1]
    
    cookiesdir= config.get_setting("cookies.dir") 
    if cookiesdir == config.get_data_path(): cookiesdir = os.path.join(cookiesdir,"Cookies")
    ficherocookies = os.path.join(cookiesdir, dominio + ".dat" )
    
    #headers por defecto si no se especifica otra cosa:
    if headers ==None:
      headers =[]
      headers.append(['User-Agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12'])
      headers.append(["Accept","text/html;charset=UTF-8"])
      headers.append(["Accept-Charset","UTF-8"])
      
    if addheaders != None:
      keys=[]
      for header in addheaders:
        keys.append(header[0])
        
      for header in headers:
        if header[0] in keys:
          headers.remove(header)
      headers.extend(addheaders) 
    if cookies==True:
      try:
        import cookielib
      except:
        cookies = False
        
    if timeout ==None:
      timeout = 25
        
    logger.info("----------------------------------------------")
    logger.info("[scrapertools.py] - downloadpage")
    logger.info("----------------------------------------------")
    if timeout is None:
      logger.info("Timeout: Sin timeout")
    else:        
      logger.info("Timeout: " + str(timeout))
    logger.info("URL: " + url)
    logger.info("Dominio: " + dominio)
    logger.info("Headers:" )
    for header in headers:
      logger.info("--------->"+header[0] + ":" + header[1])
      
    if post is not None:
        logger.info("Peticion: POST" )
        logger.info("Post: " + post)
    else:
        logger.info("Peticion: GET")
    
    if cookies==True:
        logger.info("Usar Cookies: Si")
        logger.info("Fichero de Cookies: " + ficherocookies)
    else:
        logger.info("Usar Cookies: No")
  
    
    # ---------------------------------
    # Instala las cookies
    # ---------------------------------
    if cookies==True:
      cj = cookielib.MozillaCookieJar()
      cj.set_policy(MyCookiePolicy())     
      if os.path.isfile(ficherocookies):
        logger.debug("Leyendo fichero cookies")
        try:
          cj.load(ficherocookies,ignore_discard=True)
        except:
          logger.debug("El fichero de cookies existe pero es ilegible, se borra")
          os.remove(ficherocookies)
          
      if not follow_redirects:
          opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=DEBUG_LEVEL),urllib2.HTTPCookieProcessor(cj),NoRedirectHandler())
      else:
          opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=DEBUG_LEVEL),urllib2.HTTPCookieProcessor(cj))
    else:
      if not follow_redirects:
          opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=DEBUG_LEVEL),NoRedirectHandler())
      else:
          opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=DEBUG_LEVEL)) 
      
    urllib2.install_opener(opener)
    
    # -------------------------------------------------
    # Lanza la petición
    # -------------------------------------------------
    logger.debug("Realizando Peticion")
    # Contador
    inicio = time.clock()
    # Diccionario para las cabeceras
    txheaders = {}

    # Añade las cabeceras
    for header in headers:
      txheaders[header[0]]=header[1]
    req = urllib2.Request(url, post, txheaders)
    
    try:        
      handle=urllib2.urlopen(req, timeout=timeout)            
      
      logger.debug("Peticion Realizada")
      if cookies==True:
        logger.debug("Guardando cookies...")
        cj.save(ficherocookies,ignore_discard=True) #  ,ignore_expires=True
                
      # Lee los datos y cierra
      if getdata==True:
        if handle.info().get('Content-Encoding') == 'gzip':
          logger.debug("Encoding: gzip")
          logger.debug("Descomprimiendo...")
          fin = inicio
          import StringIO
          data=handle.read()
          compressedstream = StringIO.StringIO(data)
          import gzip
          gzipper = gzip.GzipFile(fileobj=compressedstream)
          data = gzipper.read()
          gzipper.close()
          logger.debug("Descomprimido")
          fin = time.clock()
        else:
          logger.debug("Encoding: Normal")
          data = handle.read()
    except urllib2.HTTPError,e:
      if e.code == 304:
        logger.info("Pagina no modificada, cargará del cache")
      else:
        logger.error("No se ha podido realizar la petición (Codigo: "+str(e.code) + ")")
      return None
    except socket.timeout, e:
        logger.info("Timed Out: la pagina no ha respondido en el tiempo solicitado")
        return None
    except:
      import traceback
      logger.info(traceback.format_exc())
      return None

    return_headers = handle.info()
    logger.debug("Respuesta: " + str(handle.getcode()))
    logger.debug("Headers Respuesta:")
    getheader=""
    for header in return_headers:
        logger.debug("------------------->"+header+"="+return_headers[header])
        if header_to_get is not None:
            if header==header_to_get:
                getheader=return_headers[header]

    handle.close()
    # Tiempo transcurrido
    fin = time.clock()
    logger.info("Descargado en %d segundos " % (fin-inicio+1))

    if getheaders ==False and getdata ==True:
      return data
    elif getheaders ==True and getdata ==False:
      if header_to_get is not None:
        return getheader
      else:
        return return_headers
    elif getheaders ==True and getdata ==True:
      return data,return_headers



def getCacheFileNames(url):

    # Obtiene el directorio de la cache para esta url
    siteCachePath = getSiteCachePath(url)
        
    # Obtiene el ID de la cache (md5 de la URL)
    cacheId = get_md5(url)
        
    logger.debug("ID de Cache: "+cacheId)

    # Timestamp actual
    nowtimestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    logger.debug("Timestamp actual: "+nowtimestamp)

    # Nombre del fichero
    # La cache se almacena en una estructura CACHE + URL
    ruta = os.path.join( siteCachePath , cacheId[:2] , cacheId[2:] )
    newFile = os.path.join( ruta , nowtimestamp + ".cache" )
    logger.debug("Nuevo archivo Cache: "+newFile)
    if not os.path.exists(ruta):
        os.makedirs( ruta )

    # Busca ese fichero en la cache
    cachedFile = getCachedFile(siteCachePath,cacheId)

    return cachedFile, newFile 

# Busca ese fichero en la cache
def getCachedFile(siteCachePath,cacheId):
    mascara = os.path.join(siteCachePath,cacheId[:2],cacheId[2:],"*.cache")
    logger.debug("Mascara archivo cache: "+mascara)
    import glob
    ficheros = glob.glob( mascara )
    logger.debug("Hay %d ficheros con ese id" % len(ficheros))

    cachedFile = ""

    # Si hay más de uno, los borra (serán pruebas de programación) y descarga de nuevo
    if len(ficheros)>1:
        logger.debug("Cache inválida")
        for fichero in ficheros:
            logger.debug("Borrando "+fichero)
            os.remove(fichero)
        
        cachedFile = ""

    # Hay uno: fichero cacheado
    elif len(ficheros)==1:
        cachedFile = ficheros[0]

    return cachedFile

def getSiteCachePath(url):
    # Obtiene el dominio principal de la URL    
    dominio = urlparse.urlparse(url)[1]
    logger.debug("Dominio: "+dominio)
    
    # Crea un directorio en la cache para direcciones de ese dominio
    siteCachePath = os.path.join( CACHE_PATH , dominio )
    if not os.path.exists(CACHE_PATH):
        try:
            os.mkdir( CACHE_PATH )
        except:
            logger.error("Error al crear directorio "+CACHE_PATH)
    if not os.path.exists(siteCachePath):
        try:
            os.mkdir( siteCachePath )
        except:
            logger.error("Error al crear directorio "+siteCachePath)
    logger.debug("Ruta Cache del dominio: "+siteCachePath)
    return siteCachePath


class NoRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        infourl = urllib.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl
    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302


class MyCookiePolicy(cookielib.DefaultCookiePolicy):
    def set_ok(self, cookie, request):
        #logger.info("set_ok Cookie "+repr(cookie)+" request "+repr(request))
        #cookie.discard = False
        #cookie.
        devuelve = cookielib.DefaultCookiePolicy.set_ok(self, cookie, request)
        #logger.info("set_ok "+repr(devuelve))
        return devuelve

    def return_ok(self, cookie, request):
        #logger.info("return_ok Cookie "+repr(cookie)+" request "+repr(request))
        #cookie.discard = False
        devuelve = cookielib.DefaultCookiePolicy.return_ok(self, cookie, request)
        #logger.info("return_ok "+repr(devuelve))
        return devuelve

    def domain_return_ok(self, domain, request):
        #logger.info("domain_return_ok domain "+repr(domain)+" request "+repr(request))
        devuelve = cookielib.DefaultCookiePolicy.domain_return_ok(self, domain, request)
        #logger.info("domain_return_ok "+repr(devuelve))
        return devuelve

    def path_return_ok(self,path, request):
        #logger.info("path_return_ok path "+repr(path)+" request "+repr(request))
        devuelve = cookielib.DefaultCookiePolicy.path_return_ok(self, path, request)
        #logger.info("path_return_ok "+repr(devuelve))
        return devuelve


def printMatches(matches):
    i = 0
    for match in matches:
        logger.info("[scrapertools.py] %d %s" % (i , match))
        i = i + 1
        
def get_match(data,patron,index=0):
    matches = re.findall( patron , data , flags=re.DOTALL )
    return matches[index]

def find_single_match(data,patron,index=0):
    try:
        matches = re.findall( patron , data , flags=re.DOTALL )
        return matches[index]
    except:
        return ""

def entityunescape(cadena):
    return unescape(cadena)

def unescape(text):
    """Removes HTML or XML character references 
       and entities from a text string.
       keep &amp;, &gt;, &lt; in the source code.
    from Fredrik Lundh
    http://effbot.org/zone/re-sub.htm#unescape-html
    """
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":   
                    return unichr(int(text[3:-1], 16)).encode("utf-8")
                else:
                    return unichr(int(text[2:-1])).encode("utf-8")
                  
            except ValueError:
                logger.info("error de valor")
                pass
        else:
            # named entity
            try:
                '''
                if text[1:-1] == "amp":
                    text = "&amp;amp;"
                elif text[1:-1] == "gt":
                    text = "&amp;gt;"
                elif text[1:-1] == "lt":
                    text = "&amp;lt;"
                else:
                    print text[1:-1]
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]]).encode("utf-8")
                '''
                import htmlentitydefs
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]]).encode("utf-8")
            except KeyError:
                logger.info("keyerror")
                pass
            except:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

    # Convierte los codigos html "&ntilde;" y lo reemplaza por "ñ" caracter unicode utf-8
def decodeHtmlentities(string):
    string = entitiesfix(string)
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")

    def substitute_entity(match):
        from htmlentitydefs import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            return unichr(int(ent)).encode('utf-8')
        else:
            cp = n2cp.get(ent)

            if cp:
                return unichr(cp).encode('utf-8')
            else:
                return match.group()
                
    return entity_re.subn(substitute_entity, string)[0]
    
def entitiesfix(string):
    # Las entidades comienzan siempre con el símbolo & , y terminan con un punto y coma ( ; ).
    string = string.replace("&aacute","&aacute;")
    string = string.replace("&eacute","&eacute;")
    string = string.replace("&iacute","&iacute;")
    string = string.replace("&oacute","&oacute;")
    string = string.replace("&uacute","&uacute;")
    string = string.replace("&Aacute","&Aacute;")
    string = string.replace("&Eacute","&Eacute;")
    string = string.replace("&Iacute","&Iacute;")
    string = string.replace("&Oacute","&Oacute;")
    string = string.replace("&Uacute","&Uacute;")
    string = string.replace("&uuml"  ,"&uuml;")
    string = string.replace("&Uuml"  ,"&Uuml;")
    string = string.replace("&ntilde","&ntilde;")
    string = string.replace("&#191"  ,"&#191;")
    string = string.replace("&#161"  ,"&#161;")
    string = string.replace(";;"     ,";")
    return string


def htmlclean(cadena):
    cadena = cadena.replace("<center>","")
    cadena = cadena.replace("</center>","")
    cadena = cadena.replace("<cite>","")
    cadena = cadena.replace("</cite>","")
    cadena = cadena.replace("<em>","")
    cadena = cadena.replace("</em>","")
    cadena = cadena.replace("<u>","")
    cadena = cadena.replace("</u>","")
    cadena = cadena.replace("<li>","")
    cadena = cadena.replace("</li>","")
    cadena = cadena.replace("<tbody>","")
    cadena = cadena.replace("</tbody>","")
    cadena = cadena.replace("<tr>","")
    cadena = cadena.replace("</tr>","")
    cadena = cadena.replace("<![CDATA[","")
    cadena = cadena.replace("<Br />"," ")
    cadena = cadena.replace("<BR />"," ")
    cadena = cadena.replace("<Br>"," ")
    cadena = re.compile("<br[^>]*>",re.DOTALL).sub(" ",cadena)

    cadena = re.compile("<script.*?</script>",re.DOTALL).sub("",cadena)

    cadena = re.compile("<option[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</option>","")

    cadena = re.compile("<button[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</button>","")

    cadena = re.compile("<i[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</iframe>","")
    cadena = cadena.replace("</i>","")
    
    cadena = re.compile("<table[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</table>","")
    
    cadena = re.compile("<td[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</td>","")
    
    cadena = re.compile("<div[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</div>","")
    
    cadena = re.compile("<dd[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</dd>","")

    cadena = re.compile("<b[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</b>","")

    cadena = re.compile("<font[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</font>","")
    
    cadena = re.compile("<strong[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</strong>","")

    cadena = re.compile("<small[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</small>","")

    cadena = re.compile("<span[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</span>","")

    cadena = re.compile("<a[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</a>","")
    
    cadena = re.compile("<p[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</p>","")

    cadena = re.compile("<ul[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</ul>","")
    
    cadena = re.compile("<h1[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</h1>","")
    
    cadena = re.compile("<h2[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</h2>","")

    cadena = re.compile("<h3[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</h3>","")

    cadena = re.compile("<h4[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</h4>","")

    cadena = re.compile("<!--[^-]+-->",re.DOTALL).sub("",cadena)
    
    cadena = re.compile("<img[^>]*>",re.DOTALL).sub("",cadena)
    
    cadena = re.compile("<object[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</object>","")
    cadena = re.compile("<param[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</param>","")
    cadena = re.compile("<embed[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</embed>","")

    cadena = re.compile("<title[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</title>","")

    cadena = re.compile("<link[^>]*>",re.DOTALL).sub("",cadena)

    cadena = cadena.replace("\t","")
    cadena = entityunescape(cadena)
    return cadena


def slugify(title):
    
    #print title
    
    # Sustituye acentos y eñes
    title = title.replace("Á","a")
    title = title.replace("É","e")
    title = title.replace("Í","i")
    title = title.replace("Ó","o")
    title = title.replace("Ú","u")
    title = title.replace("á","a")
    title = title.replace("é","e")
    title = title.replace("í","i")
    title = title.replace("ó","o")
    title = title.replace("ú","u")
    title = title.replace("À","a")
    title = title.replace("È","e")
    title = title.replace("Ì","i")
    title = title.replace("Ò","o")
    title = title.replace("Ù","u")
    title = title.replace("à","a")
    title = title.replace("è","e")
    title = title.replace("ì","i")
    title = title.replace("ò","o")
    title = title.replace("ù","u")
    title = title.replace("ç","c")
    title = title.replace("Ç","C")
    title = title.replace("Ñ","n")
    title = title.replace("ñ","n")
    title = title.replace("/","-")
    title = title.replace("&amp;","&")

    # Pasa a minúsculas
    title = title.lower().strip()

    # Elimina caracteres no válidos 
    validchars = "abcdefghijklmnopqrstuvwxyz1234567890- "
    title = ''.join(c for c in title if c in validchars)

    # Sustituye espacios en blanco duplicados y saltos de línea
    title = re.compile("\s+",re.DOTALL).sub(" ",title)
    
    # Sustituye espacios en blanco por guiones
    title = re.compile("\s",re.DOTALL).sub("-",title.strip())

    # Sustituye espacios en blanco duplicados y saltos de línea
    title = re.compile("\-+",re.DOTALL).sub("-",title)
    
    # Arregla casos especiales
    if title.startswith("-"):
        title = title [1:]
    
    if title=="":
        title = "-"+str(time.time())

    return title


def remove_show_from_title(title,show):
    #print slugify(title)+" == "+slugify(show)
    # Quita el nombre del programa del título
    if slugify(title).startswith(slugify(show)):

        # Convierte a unicode primero, o el encoding se pierde
        title = unicode(title,"utf-8","replace")
        show = unicode(show,"utf-8","replace")
        title = title[ len(show) : ].strip()

        if title.startswith("-"):
            title = title[ 1: ].strip()
    
        if title=="":
            title = str( time.time() )
        
        # Vuelve a utf-8
        title = title.encode("utf-8","ignore")
        show = show.encode("utf-8","ignore")
    
    return title

def getRandom(str):
    return get_md5(str)


def get_filename_from_url(url):
    
    import urlparse
    parsed_url = urlparse.urlparse(url)
    try:
        filename = parsed_url.path
    except:
        # Si falla es porque la implementación de parsed_url no reconoce los atributos como "path"
        if len(parsed_url)>=4:
            filename = parsed_url[2]
        else:
            filename = ""

    return filename

def get_domain_from_url(url):
    
    import urlparse
    parsed_url = urlparse.urlparse(url)
    try:
        filename = parsed_url.netloc
    except:
        # Si falla es porque la implementación de parsed_url no reconoce los atributos como "path"
        if len(parsed_url)>=4:
            filename = parsed_url[1]
        else:
            filename = ""

    return filename

# Parses the title of a tv show episode and returns the season id + episode id in format "1x01"
def get_season_and_episode(title):
    logger.info("get_season_and_episode('"+title+"')")

    patron ="(\d+)[x|X](\d+)"
    matches = re.compile(patron).findall(title)
    logger.info(str(matches))
    filename=matches[0][0]+"x"+matches[0][1]

    logger.info("get_season_and_episode('"+title+"') -> "+filename)
    
    return filename

def get_sha1(cadena):
    try:
        import hashlib
        devuelve = hashlib.sha1(cadena).hexdigest()
    except:
        import sha
        import binascii
        devuelve = binascii.hexlify(sha.new(cadena).digest())
    
    return devuelve

def get_md5(cadena):
    try:
        import hashlib
        devuelve = hashlib.md5(cadena).hexdigest()
    except:
        import md5
        import binascii
        devuelve = binascii.hexlify(md5.new(cadena).digest())
    
    return devuelve

