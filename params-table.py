
#Generates the interior of a LaTeX table of parameters from selected runs

import sys


dirs = sys.argv[1:]


params = {}

for dir_p in dirs:
    f = open(dir_p + '/params.txt')
    for line in f.readlines():
	name = line.split()[0]
	value = line.split()[2]
	try:
	    params[name].append(value)
	except KeyError:
	    params[name] = [value]
    f.close()


rows = [
('transposition_mutation_stdev'	,	'$\\mu$',		'Transposition-related mutation stdev'),
('no_phenotype_properties'	,	'$n$',			'Dimension of phenotypic space'),
('transposition_mutation_stdev'  ,	'$\\mu$',		'Transposon-related mutation stdev'),
('non_transposition_mutation_stdev' ,	'$\\nu$',		'Non-transposon-related mutation stdev'),
('random_mutation_rate'		,	'$\\rho$',		'Non-transposon-related mutation rate'),
('niche_size'                    ,       '$m$',			'Niche size'),
('deauton_probability'		,	'$\\Delta_\\alpha$',	'Autonomy loss probability'),
('inactivation_probability'	,	'$\\Delta_\\beta$',	'Deletion probability'),
('transposition_rate'		,	'$\\tau$',		'Transposition rate'),
('model'				,	'model',	'model'),
('pint', 'pint', 'pint')]

for (key, col2, col1) in rows:
    print col1, '	&', col2, '	',
    for val in params[key]:
    	print '&', val, '	',
    print '\\\\'

    
