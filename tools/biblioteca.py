# Genera biblioteca.json (toda la biblioteca) a partir de la transcripción de fotos,
# la ruta de La mesa y los libros del lote 5 que solo figuran en el documento.
import json, re, unicodedata
FOTOS='/home/claude/la-mesa/biblioteca-fotos.md'; RUTA='/home/claude/la-mesa/seed.json'
def norm(s): return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn')
libros=[]
def clave(a,t):
    a=re.split(r'[ ,–-]',norm(a).strip())[0]; t=re.sub(r'\(.*?\)','',norm(t)); t=re.sub(r'[^a-z0-9]','',t)
    return a+'|'+t[:60]
def add(autor,titulo,area=None):
    k=clave(autor,titulo)
    for b in libros:
        if clave(b['a'],b['t'])==k:
            if area and not b['area']: b['area']=area
            return
    libros.append({'a':autor.strip(),'t':titulo.strip(),'area':area})
for line in open(FOTOS):
    m=re.match(r'- (.+?) — (.+)$',line.strip())
    if m and not line.startswith('- ¿?'): add(m.group(1),m.group(2))
    elif m:
        t=m.group(2)
        if 'fino amarillo' in t: add('Panchishkin–Shavgulidze','Trigonometric Functions (Problem-Solving Approach) (Mir)')
        elif 'Questions and Problems' in t: add('Butuzov (ed.)',t)
        elif 'High-School Mathematics' in t: add('Yakovlev (ed.)',t)
        else: add('Autor sin identificar',t)
# lote 5 y otros que solo están en el documento
LOTE5=[("de Diego–Llerena–Llerena","Problemas de oposiciones: Matemáticas, tomo 3 (Deimos)"),("de Diego et al.","Problemas de oposiciones: Matemáticas, tomo 4 (Deimos)"),
("de Diego–Gordillo","Problemas de oposiciones: Matemáticas, tomo 9 (Deimos)"),("de Diego et al.","Problemas de oposiciones: Formación Profesional (Deimos)"),
("de Diego","Ejercicios de análisis (Deimos)"),("Sánchez Torres","Problemas matemáticos resueltos de nivel avanzado"),
("Anzola–Caruncho–Pérez-Canales","Problemas de Álgebra 1: Conjuntos, grupos"),("Anzola–Caruncho–Pérez-Canales","Problemas de Álgebra 2: Anillos, polinomios, ecuaciones"),("Anzola–Caruncho–Pérez-Canales","Problemas de Álgebra 3: Espacios vectoriales"),
("Navarro","Un curso de álgebra"),("Aroca–Fernández–Pérez","Problemas de álgebra lineal (Valladolid)"),("Aroca–Fernández–Pérez","Problemas de geometría afín y geometría métrica (Valladolid)"),
("Kirkwood–Kirkwood","Elementary Linear Algebra"),("Loehr","Advanced Linear Algebra"),("Roberts","Linear Algebra"),
("Pogorelov","Geometry"),("Pogorelov","Geometría elemental"),("Hadamard","Lessons in Geometry I"),("Pamfilos","Lectures on Euclidean Geometry, vol. 1"),("Pamfilos","Lectures on Euclidean Geometry, vol. 2"),
("Altshiller-Court","College Geometry"),("Byer–Lazebnik–Smeltzer","Methods for Euclidean Geometry"),("Yaglom","Números complejos y sus aplicaciones a la geometría"),
("Postnikov","Lectures in Geometry I: Analytic Geometry"),("Postnikov","Lectures in Geometry II: Linear Algebra and Differential Geometry"),("Postnikov","Lectures in Geometry III: Smooth Manifolds"),("Postnikov","Lectures in Geometry V: Lie Groups and Lie Algebras"),
("Ilyin–Poznyak","Fundamentos del análisis matemático 1"),("Ilyin–Poznyak","Fundamentos del análisis matemático 2"),("Ilyin–Poznyak","Fundamentos del análisis matemático 3"),
("Smirnov","Curso de matemáticas superiores 1"),("Smirnov","Curso de matemáticas superiores 2"),("Smirnov","Curso de matemáticas superiores 3"),
("Ghorpade–Limaye","A Course in Calculus and Real Analysis"),("Wu","Pre-Calculus, Calculus, and Beyond"),("Marsden–Tromba","Vector Calculus"),("Shurman","Calculus and Analysis in Euclidean Space"),
("Petrovic","Advanced Calculus"),("Erdman","A Problems Based Course in Advanced Calculus"),("Taylor","Foundations of Analysis"),("Ginzburg","Brief Calculus"),("Boyadzhiev","Special Techniques for Solving Integrals"),
("Cordero–Gómez–Vázquez","Ecuaciones diferenciales: métodos analíticos y numéricos"),("Autor sin identificar","Análisis numérico"),("DiBenedetto","Real Analysis"),
("Feller","An Introduction to Probability Theory and Its Applications"),("Taylor","Games, Gambling, and Probability"),("Karr","Probability"),
("Mollin","Elementary Number Theory"),("Engel","Problem-Solving Strategies"),("Kedlaya–Poonen–Vakil","The William Lowell Putnam Mathematical Competition 1985–2000"),
("Andreescu–Dospinescu","Straight from the Book"),("Andreescu et al.","Sums and Products"),("Andreescu–Rolínek–Tkadlec","106 Geometry Problems"),("Andreescu–Rolínek–Tkadlec","107 Geometry Problems"),
("Andreescu et al.","112 Combinatorial Problems"),("Eremin","150 problemas"),("Gillman (ed.)","A Friendly Mathematics Competition"),
("Rozenblyum","Learning Trigonometry by Problem Solving"),("Litvinenko–Mordkovich","Solving Problems in Algebra and Trigonometry (Mir)"),("Gusev–Litvinenko–Mordkovich","Solving Problems in Geometry (Mir)"),
("Weiss","Secondary Mathematics for Mathematicians and Educators"),("Rey Pastor–Babini","Historia de la matemática 1"),("Rey Pastor–Babini","Historia de la matemática 2"),
("Davis–Hersh","Experiencia matemática"),("Mason–Burton–Stacey","Pensar matemáticamente"),("Decker–Pfister","A First Course in Computational Algebraic Geometry"),
("Coxeter","The Real Projective Plane"),("Gelca–Onişor–Shine","Geometric Transformations")]
for a,t in LOTE5: add(a,t)
d=json.load(open(RUTA))
for l in d['ruta']['lineas']:
    for e in l.get('etapas',[]):
        for b in e.get('libros',[]):
            if l['nombre']=='Oposiciones' or b['autor'].startswith('Asensio'): continue
            if b['autor'].startswith('Postnikov'):
                for x in libros:
                    if x['a']=='Postnikov' and ('III:' in x['t'] or ' V:' in x['t']): x['area']='mesa:'+l['nombre']
                continue
            add(b['autor'],b['titulo'],'mesa:'+l['nombre'])
# papeles en la poda (primera coincidencia gana; se buscan en autor+título)
ROLES=[
 ('temas',['Freud','Postnikov|Lectures in Geometry I:','Postnikov|Lectures in Geometry II:','Pamfilos|vol. 1','Greenleaf|Linear Algebra I (','Anzola','Ghorpade','Smirnov','Hahn','Cordero','Linde','Merris','Boolos','Coşkun']),
 ('problemas',['Deimos','Sánchez Torres','De Koninck, Mercier','Aroca','Geometric Inequalities','106 Geometry','Cacoullos','112 Combinatorial','Putnam and Beyond','Ejercicios de análisis','Panchishkin','115 Trigonometry']),
 ('consulta',['Andreescu, Andrica','Herman','Campbell','Akopyan','Hadamard','Byer','Alsina','Greenleaf|Linear Algebra II','Weintraub','Kirkwood','Loehr','Kurosh','Chirskii','Litvinenko','Wu|','Krantz','Bonar','Andreescu, Ventullo','Erdman','Nitecki','Taylor|Complex Variables','Gordon','Boyadzhiev','Karr','Wasserman','Davis–Hersh','Weiss','Gelca–Onişor','Gelca, Onişor','Mihalescu','Yaglom','Hartshorne|Euclid','Fuchs, Tabachnikov','Martínez Verduch','Montiel','Mason','Engel','Saff','Navarro','Butuzov','Mathematical Analysis in Questions','117 Polynomial','Hausner','Altshiller']),
 ('reserva',['Mollin','Dospinescu, Mushkarov','Pamfilos|vol. 2','107 Geometry','Lemmas','Roberts','Isaacs|Algebra:','Rozenblyum','Sohrab','Fischer','Taylor|Foundations','Silva','Ilyin','Shurman','Amann','Evans','Kinney','Feller','Games, Gambling','Adams, Guillemin','Pruim','Khoury','Bumbăcea','Coxeter','Wylie','Pogorelov']),
]
def match(b,pat):
    s=b['a']+' '+b['t']
    if '|' in pat:
        a,t=pat.split('|'); return a in b['a'] and t in b['t']
    return pat in s
for b in libros:
    b['rol']='estanteria'
    if b['area'] and b['area'].startswith('mesa:'): b['rol']='mesa'
    for rol,pats in ROLES:
        if any(match(b,p) for p in pats): b['rol']=rol; break
out=[{'a':b['a'],'t':b['t'],'r':b['rol']} for b in libros]
out.sort(key=lambda b:norm(b['a']))
json.dump(out,open('/home/claude/el-sorteo/tools/biblioteca.json','w'),ensure_ascii=False)
from collections import Counter; print(len(out),Counter(b['r'] for b in out))
