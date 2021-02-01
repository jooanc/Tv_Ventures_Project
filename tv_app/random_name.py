import random

last_names = ["SMITH", "JOHNSON", "WILLIAMS", "BROWN", "JONES", "GARCIA", "MILLER", "DAVIS", "RODRIGUEZ", "MARTINEZ", "HERNANDEZ", "LOPEZ", "GONZALEZ", "WILSON", "ANDERSON", "THOMAS", "TAYLOR", "MOORE", "JACKSON", "MARTIN", "LEE", "PEREZ", "THOMPSON", "WHITE", "HARRIS", "SANCHEZ", "CLARK", "RAMIREZ", "LEWIS", "ROBINSON", "WALKER", "YOUNG", "ALLEN", "KING", "WRIGHT", "SCOTT", "TORRES", "NGUYEN", "HILL", "FLORES", "GREEN", "ADAMS", "NELSON", "BAKER", "HALL", "RIVERA", "CAMPBELL", "MITCHELL", "CARTER", "ROBERTS"]
male_first_names = ["LIAM", "NOAH", "OLIVER", "WILLIAM", "ELIJAH", "JAMES", "BENJAMIN", "LUCAS", "MASON", "ETHAN", "ALEXANDER", "HENRY", "JACOB", "MICHAEL", "DANIEL", "LOGAN", "JACKSON", "SEBASTIAN", "JACK", "AIDEN", "OWEN", "SAMUEL", "MATTHEW", "JOSEPH", "LEVI", "MATEO", "DAVID", "JOHN", "WYATT", "CARTER", "JULIAN", "LUKE", "GRAYSON", "ISAAC", "JAYDEN", "THEODORE", "GABRIEL", "ANTHONY", "DYLAN", "LEO", "LINCOLN", "JAXON", "ASHER", "CHRISTOPHER", "JOSIAH", "ANDREW", "THOMAS", "JOSHUA", "EZRA", "HUDSON"]
female_first_names = ["OLIVIA", "EMMA", "AVA", "SOPHIA", "ISABELLA", "CHARLOTTE", "AMELIA", "MIA", "HARPER", "EVELYN", "ABIGAIL", "EMILY", "ELLA", "ELIZABETH", "CAMILA", "LUNA", "SOFIA", "AVERY", "MILA", "ARIA", "SCARLETT", "PENELOPE", "LAYLA", "CHLOE", "VICTORIA", "MADISON", "ELEANOR", "GRACE", "NORA", "RILEY", "ZOEY", "HANNAH", "HAZEL", "LILY", "ELLIE", "VIOLET", "LILLIAN", "ZOE", "STELLA", "AURORA", "NATALIE", "EMILIA", "EVERLY", "LEAH", "AUBREY", "WILLOW", "ADDISON", "LUCY", "AUDREY", "BELLA"]

def generate_first_name():
    if random.randint(0,1) == 0:
        return female_first_names[random.randint(0,49)]
    else :
        return male_first_names[random.randint(0,49)]

def generate_male_first_name():
    return male_first_names[random.randint(0,49)]

def generate_female_first_name():
    return female_first_names[random.randint(0,49)]

def generate_last_names():
    return last_names[random.randint(0,49)]

