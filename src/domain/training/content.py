
# Domain content extracted from kickboxing-trainer-final-v2 (2).jsx

TECHNIQUES = {
  'fr': {
    'punches': ['Jab', 'Direct', 'Crochet', 'Uppercut', 'Overhand'],
    'kicks': ['Low kick', 'Middle kick', 'High kick', 'Front kick', 'Side kick', 'Roundhouse kick'],
    'knees': ['Genou direct', 'Genou circulaire', 'Genou sauté'],
    'elbows': ['Coude horizontal', 'Coude descendant', 'Coude remontant', 'Coude rotatif'],
    'combos': [
      'Jab - Direct - Crochet',
      'Jab - Direct - Low kick',
      'Direct - Crochet - Middle kick',
      'Jab - Direct - Uppercut - Crochet',
      'Low kick - Direct - Crochet',
      'Crochet - Uppercut - High kick'
    ]
  },
  'en': {
    'punches': ['Jab', 'Cross', 'Hook', 'Uppercut', 'Overhand'],
    'kicks': ['Low kick', 'Middle kick', 'High kick', 'Front kick', 'Side kick', 'Roundhouse kick'],
    'knees': ['Straight knee', 'Circular knee', 'Flying knee'],
    'elbows': ['Horizontal elbow', 'Downward elbow', 'Uppercut elbow', 'Spinning elbow'],
    'combos': [
      'Jab - Cross - Hook',
      'Jab - Cross - Low kick',
      'Cross - Hook - Middle kick',
      'Jab - Cross - Uppercut - Hook',
      'Low kick - Cross - Hook',
      'Hook - Uppercut - High kick'
    ]
  },
  'es': {
    'punches': ['Jab', 'Directo', 'Gancho', 'Uppercut', 'Overhand'],
    'kicks': ['Patada baja', 'Patada media', 'Patada alta', 'Patada frontal', 'Patada lateral', 'Patada circular'],
    'knees': ['Rodilla directa', 'Rodilla circular', 'Rodilla saltando'],
    'elbows': ['Codo horizontal', 'Codo descendente', 'Codo ascendente', 'Codo giratorio'],
    'combos': [
      'Jab - Directo - Gancho',
      'Jab - Directo - Patada baja',
      'Directo - Gancho - Patada media',
      'Jab - Directo - Uppercut - Gancho',
      'Patada baja - Directo - Gancho',
      'Gancho - Uppercut - Patada alta'
    ]
  }
}

EXERCISES = {
  'fr': {
    'plank': 'Gainage dynamique',
    'abs': 'Abdominaux',
    'pushups': 'Pompes',
    'burpees': 'Burpees',
    'squats': 'Squats',
    'jumpingJacks': 'Jumping jacks'
  },
  'en': {
    'plank': 'Dynamic plank',
    'abs': 'Crunches',
    'pushups': 'Push-ups',
    'burpees': 'Burpees',
    'squats': 'Squats',
    'jumpingJacks': 'Jumping jacks'
  },
  'es': {
    'plank': 'Plancha dinámica',
    'abs': 'Abdominales',
    'pushups': 'Flexiones',
    'burpees': 'Burpees',
    'squats': 'Sentadillas',
    'jumpingJacks': 'Saltos de tijera'
  }
}

SPARRING_CONFIGS = {
  'muayThai': {
    'name': { 'fr': 'Muay Thaï', 'en': 'Muay Thai', 'es': 'Muay Thai' },
    'rounds': 5,
    'workTime': 180,
    'restTime': 60
  },
  'karateWKF': {
    'name': { 'fr': 'Karaté WKF', 'en': 'Karate WKF', 'es': 'Karate WKF' },
    'rounds': 3,
    'workTime': 90,
    'restTime': 60
  },
  'boxing': {
    'name': { 'fr': 'Boxe Anglaise', 'en': 'Boxing', 'es': 'Boxeo' },
    'rounds': 12,
    'workTime': 180,
    'restTime': 60
  },
  'fullContact': {
    'name': { 'fr': 'Full-Contact', 'en': 'Full-Contact', 'es': 'Full-Contact' },
    'rounds': 5,
    'workTime': 120,
    'restTime': 60
  },
  'kickboxing': {
    'name': { 'fr': 'Kickboxing', 'en': 'Kickboxing', 'es': 'Kickboxing' },
    'rounds': 5,
    'workTime': 180,
    'restTime': 60
  }
}
