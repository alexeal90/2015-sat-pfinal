from django.shortcuts import render
from django.conf.urls import patterns, include, url
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
import urllib2
import htmllib
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
from models import Usuario, Actividade, FechAdd
#from xml.sax.handler import ContentHandler
#from xml.sax import make_parser
#from xml.dom import minidom

fecha_actualiz = datetime.now()

#------------------------------------------------------------------------------------------#

def findTitle(event):
	title = event.split("<br>")[1].split('<atributo nombre="TITULO">')[1].split('</atributo>')[0]
	return title

def findKind(event):
	kind = event.split("<br>")
	auxT = kind
	i = 0
	for tp in kind:
		if tp.find('<atributo nombre="TIPO">') != -1:
			kind = event.split("<br>")[i].split('<atributo nombre="TIPO">')[1].split('</atributo>')[0]
			kind = kind.split("/")[3]
			break
		i += 1
	if auxT == kind:
		kind = "Evento"
	return kind

def findPrice(event):
	if event.split("<br>")[2] == ('<atributo nombre="GRATUITO">1</atributo>'):
		precio = event.split("<br>")[2].split('<atributo nombre="GRATUITO">')[1].split('</atributo>')[0]
		precio = "gratuito"
	elif event.split("<br>")[2] == ('<atributo nombre="GRATUITO">0</atributo>'):
		precio = event.split("<br>")
		auxPr = ""
		i = 0
		for pr in precio:
			if pr.find('<atributo nombre="PRECIO">') != -1:
				auxPr = event.split("<br>")[i].split('<atributo nombre="PRECIO">')[1].split('</atributo>')[0]
				precio = auxPr
				break
			i += 1
		if auxPr == "":
			precio = "null"
	else:
		precio = event.split("<br>")[2].split('<atributo nombre="PRECIO">')[1].split('</atributo>')[0]
		
		#precio = precio.split('<![CDATA[')[1].split(']')[0]
	return precio

def findDate(event):
	fecha = event.split("<br>")
	i = 0
	for fc in fecha:
		if fc.find('<atributo nombre="FECHA-EVENTO">') != -1:
			break
		i += 1
	fecha = event.split("<br>")[i].split('<atributo nombre="FECHA-EVENTO">')[1].split('</atributo>')[0]
	fecha = fecha.split(' ')[0]
	return fecha

def findStart(event):
	start = event.split("<br>")
	i = 0
	for h in start:
		if h.find('<atributo nombre="HORA-EVENTO">') != -1:
			break
		i += 1
	start = event.split("<br>")[i].split('<atributo nombre="HORA-EVENTO">')[1].split('</atributo>')[0]
	return start

def findLength(event):
	inicio = findStart(event)
	fin = "23:59"
	fecha_inicio = datetime.strptime(inicio, '%H:%M')
	fecha_fin = datetime.strptime(fin, '%H:%M')
	length = fecha_fin - fecha_inicio
	return length

def istooLong(length):
	tiempomin = timedelta(hours=3)
	if length >= tiempomin:
		return True
	else:
		return False

def findUrl(event):
	url = event.split("<br>")
	i = 0
	for u in url:
		if u.find('<atributo nombre="CONTENT-URL">') != -1:
			break
		i += 1
	url = event.split("<br>")[i].split('<atributo nombre="CONTENT-URL">')[1].split('</atributo>')[0]
	return url

#------------------------------------------------------------------------------------------#

def parseador():
	salida = ""
	xml = urllib2.urlopen("http://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.xml")
	xmlsoup = BeautifulSoup(xml)
	for evento in xmlsoup.findAll("contenido"):
		currEvent = ""
		for even in evento.findAll("atributo"):
			currEvent += str(even) + "<br>"
		title = findTitle(currEvent)
		kind = findKind(currEvent)
		price = findPrice(currEvent)
		date = findDate(currEvent)
		length = findLength(currEvent)
		toolong = istooLong(length)
		url = findUrl(currEvent)
		start = findStart(currEvent)
		try:
			Actividade.objects.get(title=title)
		except Actividade.DoesNotExist:
			currentAct = Actividade(title = str(title), \
								kind = str(kind), \
								price = str(price), \
								date = str(date), \
								length = str(length),\
								toolong = str(toolong), \
								url = str(url), \
								start = str(start))
			currentAct.save()    

		salida += currEvent + "<br><hr><br>"

	global fecha_actualiz
	fecha_actualiz = datetime.now()
	
	return salida

def Ordenadas(actividades):
	listaOrdenada = ""
	for actividad in actividades:
		listaOrdenada += actividad.title +" |PRECIO: "+ actividad.price +" |FECHA: "+\
		actividad.date +" |DURACION: "+ actividad.length + "<br><br>"
		
	return listaOrdenada

def init(request):
	parseador()
	actividades = Actividade.objects.order_by('-date')
	otras = Usuario.objects.all()
	response = ""
	particulares = ""
	if request.user.is_authenticated():
		log = "Hola, " + "<a href='http://127.0.0.1:8000/" + request.user.username + "'>" +\
			request.user.username + "</a>" + ". <a href='http://127.0.0.1:8000/admin/logout/'>Logout</a><br>"
	else:
		log = "<br><br>No estas logueado. <a href='http://127.0.0.1:8000/login'>Logueate</a><br>"

	for actividad in range(0,10):
		response += "TITULO: " + actividades[actividad].title + " <br>|PRECIO: " + \
							actividades[actividad].price + " <br>|FECHA: " + actividades[actividad].date + \
							" <br>|INICIO: " + actividades[actividad].start + \
							" <br>|DURACION: " + actividades[actividad].length + \
							" <br>|URL: " + "<a href=" + actividades[actividad].url + ">" + \
							actividades[actividad].url + "</a> :" + "<br><br>"
	for otra in otras:
		if otra.name != "":
			particulares += "<a href='http://127.0.0.1:8000/" + str(otra.name) + "'>" + str(otra.name) + "</a>" + ": <ul> " + \
							'<li type="circle">Nombre de la pagina: ' + str(otra.event) + "</li>" +\
							'<li type="circle">Lista de actividades:<br>' + Ordenadas(otra.actividades.all()) +"</li>" +\
							"</ul>"
	try:
		usuario = Usuario.objects.get(name = str(request.user.username))
		color_fondo = usuario.fondo
		color_letra = usuario.letra
	except Usuario.DoesNotExist:
		color_fondo = ""
		color_letra = ""

	template=get_template("index.html")
	diccionario = {"user": log, "recurso": response, "partic": particulares, "colLet": color_letra, "colBack": color_fondo} 	 	
	return HttpResponse(template.render(Context(diccionario)))

#------------------------------------------------------------------------------------------#

def add(idact):
	button = "<form action='/add' method='POST'>"
	button += "<button name='Identificador' value='"+ str(idact) +"' id='Identificador'>Add</button>"
	button += "</form>"
	return button


def actOrdenadas(request, actividades):
	if request.user.is_authenticated():
		listaOrdenada = ""
		for actividad in actividades:
			listaOrdenada += actividad.title +" |PRECIO: "+ actividad.price +" |FECHA: "+\
			actividad.date +" |DURACION: "+ actividad.length + add(actividad.id) + "<br><br>"
	else:
		listaOrdenada = ""
		for actividad in actividades:
			listaOrdenada += actividad.title +" |PRECIO: "+ actividad.price +" |FECHA: "+\
			actividad.date +" |DURACION: "+ actividad.length + "<br><br>"

	return listaOrdenada

@csrf_exempt
def ordenar(request):
	global fecha_actualiz
	
	form = "<form action='' method='POST'>\n"
	form += "Ordenar eventos por: <select name='orderby'"
	form += "<option selected value=''>"
	form += "<option value='title'> Titulo </option>"
	form += "<option value='length'> Duracion </option>"
	form += "<option value='date'> Fecha </option>"
	form += "<option value='price'> Precio </option>"  
	form += "<input type='submit' value='Reordena!'>\n"
	form += "</form>\n"
	if request.user.is_authenticated():
		log = "Hola, " + "<a href='http://127.0.0.1:8000/" + request.user.username + "'>" +\
			request.user.username + "</a>" + ". <a href='http://127.0.0.1:8000/admin/logout/'>Logout</a><br>"
		hora = "Fecha ultima actualizacion: " + str(fecha_actualiz).split(".")[0]
		numAct = "Numero de actividades: " + str(Actividade.objects.count())
		button = "<form action='/actualizar' method='POST'>"
		button += "<button name='' value=''>Actualiza!</button>"
		button += "</form>"
	else:
		log = "<br><br>No estas logueado. <a href='http://127.0.0.1:8000/login'>Logueate</a><br>"
		hora = ""
		numAct = ""
		button = ""

	if request.method == "POST":
		filtro = request.POST['orderby']
		if filtro == "date":
			ordenadas = Actividade.objects.order_by("-date")
		else:
			ordenadas = Actividade.objects.order_by(filtro)
		response = actOrdenadas(request, ordenadas)
	else:
		ordenadas = Actividade.objects.all()
		response = actOrdenadas(request, ordenadas)
	
	try:
		usuario = Usuario.objects.get(name = str(request.user.username))
		color_fondo = usuario.fondo
		color_letra = usuario.letra
	except Usuario.DoesNotExist:
		color_fondo = ""
		color_letra = ""
	
	template=get_template("todas.html")
	diccionario = {"user": log, "recurso": response, "form": form, "hora": hora,
				"nAct": numAct, "colLet": color_letra, "colBack": color_fondo, "actualiza": button} 	 	
	return HttpResponse(template.render(Context(diccionario)))
	
@csrf_exempt
def refresh(request):
    parseador()
    return HttpResponseRedirect("/todas")

#------------------------------------------------------------------------------------------#

def masDiez(username, id_acts):
	next = "<form action='/" + username + "'method='POST'>"
	next += "<button name='Ident' value='"+ str(id_acts) +"'>Siguiente pagina</button>"
	next +="</form>"
	return next

@csrf_exempt
def user(request, username):
	if request.user.is_authenticated():
		log_as = "Hola, " + "<a href='http://127.0.0.1:8000/" + request.user.username + "'>" +\
			request.user.username + "</a>" + ". <a href='http://127.0.0.1:8000/admin/logout/'>Logout</a><br>"
	else:
		log_as = "<br><br>No estas logueado. <a href='http://127.0.0.1:8000/login'>Logueate</a><br>"

	form = "<h2>Cambio nombre de la pagina personal</h2><br><br><br>"
	form += "<form action='/modcss' method='POST' id='userPage'>"
	form += "Nombre Pagina: <input type='text' name='event' value=''><br>"
	form += "Color de fondo: <input type='text' name='fondo' value=''><br>"
	form += "Color de letra: <input type='text' name='letra' value=''><br>"
	form += "<input type='submit' value='enviar'>"
	form += "</form><br>"
	
	if request.method == "GET":
		response = "<br>"
		if request.user.username == username:
			try:
				info_user = Usuario.objects.get(name=username)
				event = "<h1>Actividades de " + username + "</h1><br><h2>" + info_user.event + "</h2>"
				myactividades = info_user.actividades.all()

				if myactividades.count() > 10:
					myactividades = myactividades[:10]

				for myactividad in myactividades:
					response += "<a href='http://127.0.0.1:8000/actividad/" + str(myactividad.id) + "'>" + myactividad.title + "</a><br>"
					response += myactividad.date + "<br>"
					myfecha = FechAdd.objects.get(usuario = info_user, actividad = myactividad.id)
					response += " Se agrego en: "+ str(myfecha.fecha).split('.')[0] + "<br><br>"
					finalAct = myactividad.id

				if myactividades.count() >= 10:
            				response += masDiez(username,finalAct)

			except Usuario.DoesNotExist:
				event = ""
				response += "<h1>Pagina de usuario no encontrada</h1>"
		else:
			form = ""
			try:
				info_user = Usuario.objects.get(name=username)
				event = "<h2>Actividades de " + username + "</h3>"
				myactividades = info_user.actividades.all()

				if myactividades.count() > 10:
					myactividades = myactividades[:10]

				for myactividad in myactividades:
					response += "<a href='http://127.0.0.1:8000/actividad/" + str(myactividad.id) + "'>" + myactividad.title + "</a><br>"
					response += myactividad.date + "<br>"
					myfecha = FechAdd.objects.get(usuario = info_user, actividad = myactividad)
					response += " Se agrego en: "+ str(myfecha.fecha).split('.')[0] + "<br>"
					finalAct = myactividad.id

				if myactividades.count() >= 10:
            				response += masDiez(username,finalAct)

			except Usuario.DoesNotExist:
				event = ""
				response += "<h1>Pagina de usuario no encontrada</h1>"

		try:
			usuario = Usuario.objects.get(name = str(request.user.username))
			color_fondo = usuario.fondo
			color_letra = usuario.letra
		except Usuario.DoesNotExist:
			color_fondo = ""
			color_letra = ""

		template=get_template("personal.html")
		diccionario = {"user": log_as, "recurso": response, "form": form, "nombrePag": event, "colLet": color_letra, "colBack": color_fondo} 	 	
		return HttpResponse(template.render(Context(diccionario)))
	else:
		idUltimaAct = request.POST.get("Ident", '')
		response = "<br>"
		if request.user.username == username:
			try:
				info_user = Usuario.objects.get(name=username)
				event = "<h1>Actividades de " + username + "</h1><br><h2>" + info_user.event + "</h2>"
				myactividades = info_user.actividades.all()
				i = 0
				for myactividad in myactividades:
					if str(myactividad.id) == str(idUltimaAct):
						break
					i += 1

				i += 1

				myactividades = myactividades[i:]
				if len(myactividades) > 10:
					myactividades = myactividades[:i+10]

				i = 0
				for myactividad in myactividades:
					response += "<a href='http://127.0.0.1:8000/actividad/" + str(myactividad.id) + "'>" + myactividad.title + "</a><br>"
					response += myactividad.date + "<br>"
					myfecha = FechAdd.objects.get(usuario = info_user, actividad = myactividad.id)
					response += " Se agrego en: "+ str(myfecha.fecha).split('.')[0] + "<br><br>"
					finalAct = myactividad.id
					i += 1

				if i > 10:
            				response += masDiez(username,finalAct)

			except Usuario.DoesNotExist:
				event = ""
				response += "<h1>Pagina de usuario no encontrada</h1>"
		else:
			form = ""
			try:
				info_user = Usuario.objects.get(name=username)
				event = "<h1>Actividades de " + username + "</h1><br><h2>" + info_user.event + "</h2>"
				myactividades = info_user.actividades.all()
				i = 0
				for myactividad in myactividades:
					if str(myactividad.id) == str(idUltimaAct):
						break
					i += 1

				i += 1
				myactividades = myactividades[i:]
				if len(myactividades) > 10:
					myactividades = myactividades[:i+10]

				i = 0
				for myactividad in myactividades:
					response += "<a href='http://127.0.0.1:8000/actividad/" + str(myactividad.id) + "'>" + myactividad.title + "</a><br>"
					response += myactividad.date + "<br>"
					myfecha = FechAdd.objects.get(usuario = info_user, actividad = myactividad.id)
					response += " Se agrego en: "+ str(myfecha.fecha).split('.')[0] + "<br><br>"
					finalAct = myactividad.id
					i += 1

				if i > 10:
            				response += masDiez(username,finalAct)

			except Usuario.DoesNotExist:
				event = ""
				response += "<h1>Pagina de usuario no encontrada</h1>"
		try:
			usuario = Usuario.objects.get(name = str(request.user.username))
			color_fondo = usuario.fondo
			color_letra = usuario.letra
		except Usuario.DoesNotExist:
			color_fondo = ""
			color_letra = ""

		template=get_template("personal.html")
		diccionario = {"user": log_as, "recurso": response, "form": form, "nombrePag": event, "colLet": color_letra, "colBack": color_fondo} 	 	
		return HttpResponse(template.render(Context(diccionario)))

@csrf_exempt
def modCSS(request):
	myname = request.user
	myevent = request.POST.get("event", '')
	myCfondo = request.POST.get("fondo", '')
	myCletra = request.POST.get("letra", '')
	
	try:
		info_user = Usuario.objects.get(name = myname)
		if myevent != "":
			info_user.event = myevent
		if myCfondo != "":
			info_user.fondo = myCfondo
		if myCletra != "":
			info_user.letra = myCletra

		info_user.save()
	except Usuario.DoesNotExist:
		info_user = Usuario(name = myname, event = myevent, fondo = myCfondo, letra = myCletra)
		info_user.save()
	
	return HttpResponseRedirect("/" + str(request.user))

#------------------------------------------------------------------------------------------#

@csrf_exempt
def auth_view(request):
	if request.method == "POST":
		username = request.POST.get("username", '')
		password = request.POST.get("password", '')
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request,user)
			return HttpResponseRedirect('/')
		else:
			form = ("<h1>No existe tal cuenta. <a href='http://127.0.0.1:8000/login'>Login</a></h1><br>")
			template=get_template("login.html")
			diccionario = {"form": form}
			return HttpResponse(template.render(Context(diccionario)))
	else:
		form = "<form action='' method='POST'>"
		form += "Usuario: <input type='text' name='username' value='' id='username'><br>"
		form += "Pass: <input type='password' name='password' value='' id='password'><br>"
		form += "<input type='submit' value='enviar'>"
		form += "</form>"

		template=get_template("login.html")
		diccionario = {"form": form}
		return HttpResponse(template.render(Context(diccionario)))

#------------------------------------------------------------------------------------------#

def rss(request,username):
	if request.user.is_authenticated():
		log = log = "Hola, " + "<a href='http://127.0.0.1:8000/" + request.user.username + "'>" +\
			request.user.username + "</a>" + ". <a href='http://127.0.0.1:8000/admin/logout/'>Logout</a><br>"
	else:
		log = "<br><br>No estas logueado. <a href='http://127.0.0.1:8000/login'>Logueate</a><br>"

	try:
		user_events = Usuario.objects.get(name=username)
	except Usuario.DoesNotExist:
		return HttpResponseNotFound('<h1>Usuario no encontrado</h1>')

	event = user_events.event
	if event == None:
		response = ('<h1> no encontrado</h1>')
	else:
		actividades = user_events.actividades.all()
		resto = ""
		for actividad in actividades:
			titl = actividad.title
			resto += '\t\t<item>\n'
			resto += '\t\t\t<title>'+ str(actividad.id) + '</title>\n'
			resto += '\t\t\t<link>' + "actividad/" + str(actividad.id) + '</link>\n'
			resto += '\t\t\t<description>' + actividad.title + '</description>\n'
			resto += '\t\t</item>\n'
		
		response = '<?xml version="1.0" encoding="UTF-8"?>\n'
		response += '<rss version="2.0">\n\t<channel>\n'
		response += '\t\t<title>'+ event + '</title>\n'
		response += '\t\t<link>'+ "/" + str(username) + '</link>\n'
		response += resto
		response += '\t</channel>\n</rss>'

	return HttpResponse(response, content_type='rss')

#------------------------------------------------------------------------------------------#

def decodeToOpenUrl(url):
    u = htmllib.HTMLParser(None)
    u.save_bgn()
    u.feed(url)
    url = u.save_end()
    return url

def actividad(request,idAct):
	if request.user.is_authenticated():
		log = "Hola, " + "<a href='http://127.0.0.1:8000/" + request.user.username + "'>" +\
			request.user.username + "</a>" + ". <a href='http://127.0.0.1:8000/admin/logout/'>Logout</a><br>"
	else:
		log = "<br><br>No estas logueado. <a href='http://127.0.0.1:8000/login'>Logueate</a><br>"
	
	try:
		usuario = Usuario.objects.get(name = str(request.user.username))
		color_fondo = usuario.fondo
		color_letra = usuario.letra
	except Usuario.DoesNotExist:
		color_fondo = ""
		color_letra = ""
		
	response = ""
	try:
		actividad = Actividade.objects.get(id=idAct)
		response += actividad.title +" |PRECIO: "+ actividad.price +" |FECHA: "+\
						actividad.date +" |DURACION: "+ actividad.length + "<br><br>"
		
		urlInfor = decodeToOpenUrl(actividad.url)
		infor = urllib2.urlopen(urlInfor)
		infor = infor.read()
		s = infor.find('<div class="parrafo">')
		if s == -1:
			boolean = False
			inform = "<a href=" + str(actividad.url) + ">" + "informacion" + "</a> <br>"
		else:
			boolean = True
			e = infor.find('</div>',s)
			parrafo = infor[s:e]
			parrafoaux = parrafo.split('<div class="parrafo">')[1]
			inform = parrafoaux + "<br><a href=" + str(actividad.url) + ">" + "toda la informacion" + "</a> <br>"
			inform = unicode(inform, 'utf-8')

		if boolean == True:
			response += inform

			template=get_template("actividad.html")
			diccionario = {"user": log, "recurso": response, "idAct": idAct, "colLet": color_letra, "colBack": color_fondo} 	 	
			return HttpResponse(template.render(Context(diccionario)))
		else:
			urlAdc = decodeToOpenUrl(actividad.url)
			urlA = urllib2.urlopen(urlAdc)
			html = urlA.read()
			start = html.find('<a class="punteado" href="')
        
			if start != -1:
				urlInfor = actividad.url
			else:
				response += "<a href=" + actividad.url + ">" + "informacion no diponible" + "</a> <br>"
				end = html.find('">',start)
				parrafo = html[start:end]
				urlInfor = parrafo.split('href="')[1]

			if not urlInfor.startswith("http://www.madrid.es"):
				urlInfor = "http://www.madrid.es" + urlInfor

			urlInfor = decodeToOpenUrl(urlInfor)
			infor = urllib2.urlopen(urlInfor)
			infor = infor.read()
			s = infor.find('<div class="parrafo">')
			if s == -1:
				response += "<a href=" + urlInfor + ">" + "informacion" + "</a> <br>"
			else:       
				e = infor.find('</div>',s)
				parrafo = infor[s:e]
				response += parrafo + "<br>"
				response += "<a href=" + act.Url + ">" + "toda la informacion" + "</a> <br>"

			template=get_template("actividad.html")
			diccionario = {"user": log, "recurso": response, "idAct": idAct, "colLet": color_letra, "colBack": color_fondo} 	 	
			return HttpResponse(template.render(Context(diccionario)))
	except Actividade.DoesNotExist:
		response = "Actividad inexistente"
		template=get_template("actividad.html")
		diccionario = {"user": log, "recurso": response, "idAct": idAct, "colLet": color_letra, "colBack": color_fondo} 	 	
		return HttpResponse(template.render(Context(diccionario)))

#------------------------------------------------------------------------------------------#

def comprobar(myusuario, myactividades):
	try:
		fecha = FechAdd.objects.get(usuario = myusuario, actividad = myactividades)
		return True
	except:
		return False

@csrf_exempt
def addEve(request):
	actividad = request.POST.get("Identificador", '')
	try:
		pp = Usuario.objects.get(name = request.user)
	except Usuario.DoesNotExist:
		pp = Usuario(name = str(request.user), event = "pagina de " + str(request.user))
		pp.save()

	pagaa = Actividade.objects.get(id=actividad)
	pp.actividades.add(pagaa)
	boolean = comprobar(str(request.user),actividad)
	if not boolean:
		myusuario = Usuario.objects.get(name = str(request.user))
		myact = Actividade.objects.get(id=actividad)
		hora = datetime.now()
		publicar = FechAdd(fecha = hora, usuario = myusuario, actividad = myact)
		publicar.save()

	return HttpResponseRedirect("/todas")

def ayuda(request):
	if request.user.is_authenticated():
		log = "Hola, " + "<a href='http://127.0.0.1:8000/" + request.user.username + "'>" +\
			request.user.username + "</a>" + ". <a href='http://127.0.0.1:8000/admin/logout/'>Logout</a><br>"
	else:
		log = "<br><br>No estas logueado. <a href='http://127.0.0.1:8000/login'>Logueate</a><br>"
	
	try:
		usuario = Usuario.objects.get(name = str(request.user.username))
		color_fondo = usuario.fondo
		color_letra = usuario.letra
	except Usuario.DoesNotExist:
		color_fondo = ""
		color_letra = ""

	template=get_template("help.html")
	diccionario = {"user": log, "colLet": color_letra, "colBack": color_fondo} 	 	
	return HttpResponse(template.render(Context(diccionario)))


#def logout(request):
	#log = "<br><br>No estas logueado. <a href='http://127.0.0.1:8000/login'>Logueate</a><br>"
	#template=get_template("logout.html")
	#diccionario = {"notuser": log} 	 	
	#return HttpResponse(template.render(Context(diccionario)))
	
