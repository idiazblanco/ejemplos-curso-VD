import os 


import os
for file in os.listdir():
    if file.endswith(".py") and file.startswith('demo'):
    	print('procesando',file,' ... (generando html con highlight)')
    	os.system('pygmentize -f html -O full -o %s %s'%('./fuentes/'+file[:-3]+'_codigofuente.html',file))


