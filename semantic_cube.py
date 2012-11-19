# Cubo Semantico
import dir

cube = {
		'+':[#SUMA(+)
			[int,float,'E','E','E'],
			[float,float,'E','E','E'],
			['E','E','E','E','E'],
			['E','E','E','E','E'],
			['E','E','E','E','E']
		],
		'-':[#RESTA(-)
			[int,float,'E','E','E'],
			[float,float,'E','E','E'],
			['E','E','E','E','E'],
			['E','E','E','E','E'],
			['E','E','E','E','E']
		],
		'*':[#MULTIPLICACION(*)
			[int,float,'E','E','E'],
			[float,float,'E','E','E'],
			['E','E','E','E','E'],
			['E','E','E','E','E'],
			['E','E','E','E','E']
		],
		'/':[#DIVISION(/)
			[int,float,'E','E','E'],
			[float,float,'E','E','E'],
			['E','E','E','E','E'],
			['E','E','E','E','E'],
			['E','E','E','E','E']
		],
		'>':[#MAYORQUE(>)
			[bool,bool,'E','E','E'],
			[bool,bool,'E','E','E','E'],
			['E','E','E','E','E'],
			['E','E','E','E','E'],
			['E','E','E','E','E']
		],
		'<':[#MENORQUE(<)
			[bool,bool,'E','E','E'],
			[bool,bool,'E','E','E'],
			['E','E','E','E','E'],
			['E','E','E','E','E'],
			['E','E','E','E','E']
		],
		'<>':[#DIFERENTE(<>)
			[bool,bool,'E','E','E'],
			[bool,bool,'E','E','E'],
			['E','E',bool,'E','E'],
			['E','E','E','E','E'],
			['E','E','E','E','E']
		],
		'>=':[#MAYORIGUAL(>=)
			[bool,bool,'E','E','E'],
			[bool,bool,'E','E','E'],
			['E','E','E','E','E'],
			['E','E','E','E','E'],
			['E','E','E','E','E']
		],
		'<=':[#MENORIGUAL(<=)
			[bool,bool,'E','E','E'],
			[bool,bool,'E','E','E'],
			['E','E','E','E','E'],
			['E','E','E','E','E'],
			['E','E','E','E','E']
		],
		'and':[#AND
			[int,int,'E','E','E'],
			[int,int,'E','E','E'],
			['E','E','E','E','E'],
			['E','E','E',bool,'E'],
			['E','E','E','E','E']
		],
		'or':[#OR
			[int,int,'E','E','E'],
			[int,int,'E','E','E'],
			['E','E','E','E','E'],
			['E','E','E',bool,'E'],
			['E','E','E','E','E']
		],
		'not':[#NOT
			['E','E','E','E',int],
			['E','E','E','E',int],
			['E','E','E','E','E'],
			['E','E','E','E',bool],
			['E','E','E','E','E']
		],
		'=':[#IGUAL(=)
			[int,int,'E','E','E'],
			[float,float,'E','E','E'],
			['E','E',str,'E','E'],
			['E','E','E',bool,'E'],
			['E','E','E','E','E']
		],
		'==':[#IGUALIGUAL(==)
			[bool,bool,'E','E','E'],
			[bool,bool,'E','E','E'],
			['E','E',bool,'E','E'],
			['E','E','E',bool,'E'],
			['E','E','E','E','E']
		]
	}

def traduce_tipo(tipo):
  return {
    int: 0,
    float: 1,
    str: 2,
    bool: 3,
    None: 4,
  }[tipo]

def get_type(oper, type1, type2):
  return cube[oper][traduce_tipo(type1)][traduce_tipo(type2)]
