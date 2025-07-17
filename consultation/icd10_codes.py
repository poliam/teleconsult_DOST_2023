"""
ICD-10 code and description pairs for mental health (F00-F99)
Data from: https://github.com/StefanoTrv/simple_icd_10
"""

ICD10_MENTAL_HEALTH_CODES = {
    'F00': 'Dementia in Alzheimer disease',
    'F01': 'Vascular dementia',
    'F02': 'Dementia in other diseases classified elsewhere',
    'F03': 'Unspecified dementia',
    'F04': 'Organic amnesic syndrome, not induced by alcohol and other psychoactive substances',
    'F05': 'Delirium, not induced by alcohol and other psychoactive substances',
    'F06': 'Other mental disorders due to brain damage and dysfunction and to physical disease',
    'F07': 'Personality and behavioural disorders due to brain disease, damage and dysfunction',
    'F09': 'Unspecified organic or symptomatic mental disorder',
    'F10': 'Mental and behavioural disorders due to use of alcohol',
    'F11': 'Mental and behavioural disorders due to use of opioids',
    'F12': 'Mental and behavioural disorders due to use of cannabinoids',
    'F13': 'Mental and behavioural disorders due to use of sedatives or hypnotics',
    'F14': 'Mental and behavioural disorders due to use of cocaine',
    'F15': 'Mental and behavioural disorders due to use of other stimulants, including caffeine',
    'F16': 'Mental and behavioural disorders due to use of hallucinogens',
    'F17': 'Mental and behavioural disorders due to use of tobacco',
    'F18': 'Mental and behavioural disorders due to use of volatile solvents',
    'F19': 'Mental and behavioural disorders due to multiple drug use and use of other psychoactive substances',
    'F20': 'Schizophrenia',
    'F21': 'Schizotypal disorder',
    'F22': 'Persistent delusional disorders',
    'F23': 'Acute and transient psychotic disorders',
    'F24': 'Induced delusional disorder',
    'F25': 'Schizoaffective disorders',
    'F28': 'Other nonorganic psychotic disorders',
    'F29': 'Unspecified nonorganic psychosis',
    'F30': 'Manic episode',
    'F31': 'Bipolar affective disorder',
    'F32': 'Depressive episode',
    'F33': 'Recurrent depressive disorder',
    'F34': 'Persistent mood [affective] disorders',
    'F38': 'Other mood [affective] disorders',
    'F39': 'Unspecified mood [affective] disorder',
    'F40': 'Phobic anxiety disorders',
    'F41': 'Other anxiety disorders',
    'F42': 'Obsessive-compulsive disorder',
    'F43': 'Reaction to severe stress, and adjustment disorders',
    'F44': 'Dissociative [conversion] disorders',
    'F45': 'Somatoform disorders',
    'F48': 'Other neurotic disorders',
    'F50': 'Eating disorders',
    'F51': 'Nonorganic sleep disorders',
    'F52': 'Sexual dysfunction, not caused by organic disorder or disease',
    'F53': 'Mental and behavioural disorders associated with the puerperium, not elsewhere classified',
    'F54': 'Psychological and behavioural factors associated with disorders or diseases classified elsewhere',
    'F55': 'Abuse of non-dependence-producing substances',
    'F59': 'Unspecified behavioural syndromes associated with physiological disturbances and physical factors',
    'F60': 'Specific personality disorders',
    'F61': 'Mixed and other personality disorders',
    'F62': 'Enduring personality changes, not attributable to brain damage and disease',
    'F63': 'Habit and impulse disorders',
    'F64': 'Gender identity disorders',
    'F65': 'Disorders of sexual preference',
    'F66': 'Psychological and behavioural disorders associated with sexual development and orientation',
    'F68': 'Other disorders of adult personality and behaviour',
    'F69': 'Unspecified disorder of adult personality and behaviour',
    'F70': 'Mild mental retardation',
    'F71': 'Moderate mental retardation',
    'F72': 'Severe mental retardation',
    'F73': 'Profound mental retardation',
    'F78': 'Other mental retardation',
    'F79': 'Unspecified mental retardation',
    'F80': 'Specific developmental disorders of speech and language',
    'F81': 'Specific developmental disorders of scholastic skills',
    'F82': 'Specific developmental disorder of motor function',
    'F83': 'Mixed specific developmental disorders',
    'F84': 'Pervasive developmental disorders',
    'F88': 'Other disorders of psychological development',
    'F89': 'Unspecified disorder of psychological development',
    'F90': 'Hyperkinetic disorders',
    'F91': 'Conduct disorders',
    'F92': 'Mixed disorders of conduct and emotions',
    'F93': 'Emotional disorders with onset specific to childhood',
    'F94': 'Disorders of social functioning with onset specific to childhood and adolescence',
    'F95': 'Tic disorders',
    'F98': 'Other behavioural and emotional disorders with onset usually occurring in childhood and adolescence',
    'F99': 'Mental disorder, not otherwise specified'
}

def search_mental_health_codes(query):
    """
    Search ICD-10 codes and descriptions for mental health codes (F00-F99)
    Returns matches where either the code starts with the query or description contains the query
    """
    query = query.upper()
    results = []
    
    for code, description in ICD10_MENTAL_HEALTH_CODES.items():
        if code.startswith(query) or query in description.upper():
            results.append({
                'code': code,
                'description': description
            })
    
    return results
