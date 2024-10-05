# flake8: noqa: E501

import re
from typing import List

from src.utils import string as String

LEGALDEADLINES = [
    { "subject": 'parto a termo', "time": 300, },
    { "subject": 'carência máxima', "time": 180, },
]

## carencia de dias
LACKOFDAYS = r'carência de (\d+) \(.*\) dias'
LACKOFDAYSEXPIRE = r'carência excedida de (\d+) \(.*\) dias'

def execution_out_of_time(hipothesis):
    """
    """
    patterns = [
       LACKOFDAYS,
       LACKOFDAYSEXPIRE,
    ]
    
    executions: List[dict] = []
    
    for hipothese in hipothesis:
        clause = hipothese["clause"]
        for patt in patterns:
            match = re.findall(patt, clause)
            for deadline_in_clause in match:
                for legal_deadline in LEGALDEADLINES:
                    if check_deadline(deadline_in_clause, legal_deadline['time']):
                        reason = f"O prazo para {legal_deadline['subject']} excede o permitido por lei de {deadline_in_clause} para {legal_deadline['time']}."
                        executions.append({ "justification": reason })
    
    return executions
                   


def check_deadline(deadline_in_clause: int = 0, legal_deadline: int = 0)-> str:
    deadline_in_clause = int(deadline_in_clause)
    legal_deadline = int(legal_deadline)
    return legal_deadline and deadline_in_clause > legal_deadline
    


