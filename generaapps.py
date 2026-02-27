import os 


import os
for file in os.listdir():
    if file.endswith(".py") and not file.startswith('gen'):
    	print('procesando',file,' ... (generando html con highlight)')
    	os.system('python %s'%(file))


