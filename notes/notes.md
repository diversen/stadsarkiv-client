# Ønsker 

* "Kreativ ophav skal sættes på." (Backend)
* Zoom på billeder.
* Større format på billeder (backend)
* Forskellige søgeresultater for fx:

karré 211
karre 211

* "Kan man søge på arkiv-id i AarhusArkivet"

Bare til overvejelse, hvis man ikke kan.

# Manglende data

Fx: 

https://aarhusteaterarkiv-web.appspot.com/records/000314543

Denne har resources. Tilsyneladende et billede, men det vises ikke. 
Ligeledes står der at "Materialet er online her på Aarhusarkivet.dk ... "

# Rettelser: 


Sejrs samling har en masse 'records' som har Emnekategori > Natur > Åer og bække
Måske er der en mening med det, men jeg forstår den ikke. 

http://localhost:5555/search?subjects=12&

En besynderlig seddel: 

https://www.aarhusarkivet.dk/records/000097232?search=14


Manglende PDF:

https://stadsarkiv.aarhus.dk/media/17933/oplysninger-om-rent-private-forhold.pdf

Manglende side: (Ret ligeledes link i http://localhost:5555/about/privacy)

https://aarhusarkivet.dk/about/cookies

https://localhost:5555/about/cookies

https://stadsarkiv.aarhus.dk/besoeg-arkivet/besoeg-laesesalen/

Manglende https://

http://2017aarhusianere.dk/ -> redirecter til https://www.aarhusarkivet.dk/collections/213 

I det hele taget bør alle links være https://

Se fx : http://localhost:5555/collectors/100701

http://denstoredanske.dk/Dansk_Biografisk_Leksikon/Medier/Bibliotekar/Emanuel_Sejr

# Template-struktur

  - index
  - auth
      - login, logout, register, forgot-password, reset-password
  - user
      - me
  - pages
      - about, privacy, accessability, contact, how-tos...
  - search/adv. search
  - resource
      - collection, entity, record...
        - core metadata, files, relations, series, thumbnails...
  - admin


# Et par indledende overvejelser.

Software:

Pluggy (https://pluggy.readthedocs.io/en/stable/):

https://kracekumar.com/post/build_plugins_with_pluggy/

https://dev.to/waylonwalker/a-minimal-pluggy-example-3mp0

Blinker (https://blinker.readthedocs.io/en/stable/)

Pyemitter (https://pypi.org/project/pymitter/)


Hooks/signals: 
before_entity_insert 
after_entity_insert 
after_entity_get 
before_entity_revert 
after_entity_revert 
before_entity_update 
after_entity_update 
after_entity_delete 

before_render_template (GUI-response) x
    context object / 

before_json_response (Data-response) 

before_search_query x
after_search_results x
before_next_results 

# Todo

Register: Man bliver altid verificeret. 
OK: redirect ikke til login når man forsøger at logge ind uden at det lykkes. 

# records

Sejrs samling: 

000110308

Med Rettighedsnoter:

https://www.aarhusarkivet.dk/records/000125820

Admin:

http://localhost:5555/records/000186239

Ordering: 

https://www.aarhusarkivet.dk/records/000205238

Admin: 

http://localhost:5555/records/000478348

PDF:

records/000186693

## representations but no record_type

http://localhost:5555/records/000149892
http://localhost:5555/records/000149892
http://localhost:5555/records/000149864
http://localhost:5555/records/000149840
http://localhost:5555/records/000149846
http://localhost:5555/records/000149882
http://localhost:5555/records/000149861
http://localhost:5555/records/000149848
http://localhost:5555/records/000149845
http://localhost:5555/records/000149851
http://localhost:5555/records/000149862
http://localhost:5555/records/000149887
http://localhost:5555/records/000149877
http://localhost:5555/records/000149878
http://localhost:5555/records/000149854
http://localhost:5555/records/000149866


