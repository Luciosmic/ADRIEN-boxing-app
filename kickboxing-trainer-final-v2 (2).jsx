import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw, Settings, Plus, Trash2, GripVertical, Volume2, Edit2, Save, X, Download, Upload, Bell, SkipForward, ChevronsRight, Copy, ArrowLeft, List, Pencil } from 'lucide-react';

// Données des techniques de kickboxing par catégorie
const TECHNIQUES = {
  fr: {
    punches: ['Jab', 'Direct', 'Crochet', 'Uppercut', 'Overhand'],
    kicks: ['Low kick', 'Middle kick', 'High kick', 'Front kick', 'Side kick', 'Roundhouse kick'],
    knees: ['Genou direct', 'Genou circulaire', 'Genou sauté'],
    elbows: ['Coude horizontal', 'Coude descendant', 'Coude remontant', 'Coude rotatif'],
    combos: [
      'Jab - Direct - Crochet',
      'Jab - Direct - Low kick',
      'Direct - Crochet - Middle kick',
      'Jab - Direct - Uppercut - Crochet',
      'Low kick - Direct - Crochet',
      'Crochet - Uppercut - High kick'
    ]
  },
  en: {
    punches: ['Jab', 'Cross', 'Hook', 'Uppercut', 'Overhand'],
    kicks: ['Low kick', 'Middle kick', 'High kick', 'Front kick', 'Side kick', 'Roundhouse kick'],
    knees: ['Straight knee', 'Circular knee', 'Flying knee'],
    elbows: ['Horizontal elbow', 'Downward elbow', 'Uppercut elbow', 'Spinning elbow'],
    combos: [
      'Jab - Cross - Hook',
      'Jab - Cross - Low kick',
      'Cross - Hook - Middle kick',
      'Jab - Cross - Uppercut - Hook',
      'Low kick - Cross - Hook',
      'Hook - Uppercut - High kick'
    ]
  },
  es: {
    punches: ['Jab', 'Directo', 'Gancho', 'Uppercut', 'Overhand'],
    kicks: ['Patada baja', 'Patada media', 'Patada alta', 'Patada frontal', 'Patada lateral', 'Patada circular'],
    knees: ['Rodilla directa', 'Rodilla circular', 'Rodilla saltando'],
    elbows: ['Codo horizontal', 'Codo descendente', 'Codo ascendente', 'Codo giratorio'],
    combos: [
      'Jab - Directo - Gancho',
      'Jab - Directo - Patada baja',
      'Directo - Gancho - Patada media',
      'Jab - Directo - Uppercut - Gancho',
      'Patada baja - Directo - Gancho',
      'Gancho - Uppercut - Patada alta'
    ]
  }
};

const EXERCISES = {
  fr: {
    plank: 'Gainage dynamique',
    abs: 'Abdominaux',
    pushups: 'Pompes',
    burpees: 'Burpees',
    squats: 'Squats',
    jumpingJacks: 'Jumping jacks'
  },
  en: {
    plank: 'Dynamic plank',
    abs: 'Crunches',
    pushups: 'Push-ups',
    burpees: 'Burpees',
    squats: 'Squats',
    jumpingJacks: 'Jumping jacks'
  },
  es: {
    plank: 'Plancha dinámica',
    abs: 'Abdominales',
    pushups: 'Flexiones',
    burpees: 'Burpees',
    squats: 'Sentadillas',
    jumpingJacks: 'Saltos de tijera'
  }
};

// Configuration des sports de sparring
const SPARRING_CONFIGS = {
  muayThai: {
    name: { fr: 'Muay Thaï', en: 'Muay Thai', es: 'Muay Thai' },
    rounds: 5,
    workTime: 180,
    restTime: 60
  },
  karateWKF: {
    name: { fr: 'Karaté WKF', en: 'Karate WKF', es: 'Karate WKF' },
    rounds: 3,
    workTime: 90,
    restTime: 60
  },
  boxing: {
    name: { fr: 'Boxe Anglaise', en: 'Boxing', es: 'Boxeo' },
    rounds: 12,
    workTime: 180,
    restTime: 60
  },
  fullContact: {
    name: { fr: 'Full-Contact', en: 'Full-Contact', es: 'Full-Contact' },
    rounds: 5,
    workTime: 120,
    restTime: 60
  },
  kickboxing: {
    name: { fr: 'Kickboxing', en: 'Kickboxing', es: 'Kickboxing' },
    rounds: 5,
    workTime: 180,
    restTime: 60
  }
};

// Thèmes d'ambiance avec images de fond
const THEMES = {
  muayThaiCamp: {
    name: { fr: 'Camp Muay Thaï', en: 'Muay Thai Camp', es: 'Campo Muay Thai' },
    colors: {
      primary: '#dc2626',
      secondary: '#fbbf24',
      background: 'from-red-900 via-orange-900 to-yellow-900',
      cardBg: 'rgba(153, 27, 27, 0.7)'
    },
    backgroundImage: 'linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.6)), url("data:image/svg+xml,%3Csvg width=\'100\' height=\'100\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cdefs%3E%3Cpattern id=\'muaythai\' x=\'0\' y=\'0\' width=\'100\' height=\'100\' patternUnits=\'userSpaceOnUse\'%3E%3Crect fill=\'%23991b1b\' width=\'100\' height=\'100\'/%3E%3Ccircle cx=\'50\' cy=\'50\' r=\'40\' fill=\'%23b91c1c\' opacity=\'0.3\'/%3E%3C/pattern%3E%3C/defs%3E%3Crect fill=\'url(%23muaythai)\' width=\'100\' height=\'100\'/%3E%3C/svg%3E")'
  },
  boxingGym: {
    name: { fr: 'Salle de Boxe', en: 'Boxing Gym', es: 'Gimnasio de Boxeo' },
    colors: {
      primary: '#1e40af',
      secondary: '#dc2626',
      background: 'from-gray-900 via-blue-900 to-black',
      cardBg: 'rgba(30, 58, 138, 0.7)'
    },
    backgroundImage: 'linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), url("data:image/svg+xml,%3Csvg width=\'100\' height=\'100\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cdefs%3E%3Cpattern id=\'boxing\' x=\'0\' y=\'0\' width=\'100\' height=\'100\' patternUnits=\'userSpaceOnUse\'%3E%3Crect fill=\'%231e3a8a\' width=\'100\' height=\'100\'/%3E%3Cline x1=\'0\' y1=\'50\' x2=\'100\' y2=\'50\' stroke=\'%232563eb\' stroke-width=\'2\' opacity=\'0.3\'/%3E%3Cline x1=\'50\' y1=\'0\' x2=\'50\' y2=\'100\' stroke=\'%232563eb\' stroke-width=\'2\' opacity=\'0.3\'/%3E%3C/pattern%3E%3C/defs%3E%3Crect fill=\'url(%23boxing)\' width=\'100\' height=\'100\'/%3E%3C/svg%3E")'
  },
  okinawaDojo: {
    name: { fr: 'Dojo d\'Okinawa', en: 'Okinawa Dojo', es: 'Dojo de Okinawa' },
    colors: {
      primary: '#78350f',
      secondary: '#dc2626',
      background: 'from-amber-900 via-stone-800 to-neutral-900',
      cardBg: 'rgba(120, 53, 15, 0.7)'
    },
    // Ambiance Okinawa : tons bois naturel, bambou, zen, minimaliste
    backgroundImage: 'linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), url("data:image/svg+xml,%3Csvg width=\'200\' height=\'200\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cdefs%3E%3Cpattern id=\'okinawa\' x=\'0\' y=\'0\' width=\'200\' height=\'200\' patternUnits=\'userSpaceOnUse\'%3E%3Crect fill=\'%2378350f\' width=\'200\' height=\'200\'/%3E%3Crect x=\'10\' y=\'10\' width=\'20\' height=\'180\' fill=\'%23a16207\' opacity=\'0.3\'/%3E%3Crect x=\'40\' y=\'10\' width=\'20\' height=\'180\' fill=\'%23a16207\' opacity=\'0.3\'/%3E%3Crect x=\'70\' y=\'10\' width=\'20\' height=\'180\' fill=\'%23a16207\' opacity=\'0.3\'/%3E%3Crect x=\'100\' y=\'10\' width=\'20\' height=\'180\' fill=\'%23a16207\' opacity=\'0.3\'/%3E%3Crect x=\'130\' y=\'10\' width=\'20\' height=\'180\' fill=\'%23a16207\' opacity=\'0.3\'/%3E%3Crect x=\'160\' y=\'10\' width=\'20\' height=\'180\' fill=\'%23a16207\' opacity=\'0.3\'/%3E%3Ccircle cx=\'100\' cy=\'100\' r=\'30\' fill=\'none\' stroke=\'%23dc2626\' stroke-width=\'2\' opacity=\'0.2\'/%3E%3C/pattern%3E%3C/defs%3E%3Crect fill=\'url(%23okinawa)\' width=\'200\' height=\'200\'/%3E%3C/svg%3E")'
  }
};

const TRANSLATIONS = {
  fr: {
    title: 'Entraînement Kickboxing',
    warmup: 'Échauffement',
    jumpRope: 'Corde à sauter',
    strength: 'Musculation',
    heavyBag: 'Sac de frappe',
    shadowBoxing: 'Shadow boxing',
    cooldown: 'Étirement/Récupération',
    sparring: 'Sparring',
    start: 'Démarrer',
    pause: 'Pause',
    reset: 'Réinitialiser',
    round: 'Round',
    rest: 'Repos',
    prepare: 'Préparation',
    work: 'Travail',
    settings: 'Paramètres',
    addBlock: 'Ajouter un bloc',
    duration: 'Durée',
    rounds: 'Rounds',
    workTime: 'Temps de travail',
    restTime: 'Temps de repos',
    volume: 'Volume',
    selectTechniques: 'Sélectionner les techniques',
    punches: 'Coups de poing',
    kicks: 'Coups de pied',
    knees: 'Coups de genou',
    elbows: 'Coudes',
    combos: 'Combos',
    selectExercises: 'Sélectionner les exercices',
    reps: 'Répétitions',
    speedUp: 'Accélérez !',
    normalPace: 'Rythme normal',
    edit: 'Modifier',
    save: 'Enregistrer',
    cancel: 'Annuler',
    delete: 'Supprimer',
    duplicate: 'Dupliquer',
    rename: 'Renommer',
    language: 'Langue',
    saveWorkout: 'Sauvegarder l\'entraînement',
    loadWorkout: 'Charger',
    workoutName: 'Nom de l\'entraînement',
    myWorkouts: 'Mes entraînements',
    presetWorkouts: 'Séances',
    preset30min: 'Séance 30 minutes',
    preset60min: 'Séance 1 heure',
    preset90min: 'Séance 1h30',
    minutes: 'Minutes',
    seconds: 'Secondes',
    frequency: 'Fréquence d\'énonciation',
    slow: 'Lent (7s)',
    normal: 'Normal (5s)',
    fast: 'Rapide (3s)',
    double: 'Double',
    triple: 'Triple',
    skipRound: 'Passer au round suivant',
    skipBlock: 'Passer au bloc suivant',
    voiceProfile: 'Voix',
    trainingComplete: 'Entraînement terminé !',
    theme: 'Ambiance',
    sport: 'Sport',
    exercise: 'Exercice',
    backToTraining: 'Retour à l\'entraînement',
    noSavedWorkouts: 'Aucun entraînement sauvegardé',
    deleteConfirm: 'Supprimer cet entraînement ?',
    saveCurrentWorkout: 'Sauvegarder cet entraînement',
    createdOn: 'Créé le',
    newName: 'Nouveau nom',
    selectWorkout: 'Sélectionner un entraînement'
  },
  en: {
    title: 'Kickboxing Training',
    warmup: 'Warm-up',
    jumpRope: 'Jump rope',
    strength: 'Strength training',
    heavyBag: 'Heavy bag',
    shadowBoxing: 'Shadow boxing',
    cooldown: 'Cool-down/Stretching',
    sparring: 'Sparring',
    start: 'Start',
    pause: 'Pause',
    reset: 'Reset',
    round: 'Round',
    rest: 'Rest',
    prepare: 'Prepare',
    work: 'Work',
    settings: 'Settings',
    addBlock: 'Add block',
    duration: 'Duration',
    rounds: 'Rounds',
    workTime: 'Work time',
    restTime: 'Rest time',
    volume: 'Volume',
    selectTechniques: 'Select techniques',
    punches: 'Punches',
    kicks: 'Kicks',
    knees: 'Knees',
    elbows: 'Elbows',
    combos: 'Combos',
    selectExercises: 'Select exercises',
    reps: 'Reps',
    speedUp: 'Speed up!',
    normalPace: 'Normal pace',
    edit: 'Edit',
    save: 'Save',
    cancel: 'Cancel',
    delete: 'Delete',
    duplicate: 'Duplicate',
    rename: 'Rename',
    language: 'Language',
    saveWorkout: 'Save workout',
    loadWorkout: 'Load',
    workoutName: 'Workout name',
    myWorkouts: 'My workouts',
    presetWorkouts: 'Sessions',
    preset30min: '30-minute session',
    preset60min: '1-hour session',
    preset90min: '1h30 session',
    minutes: 'Minutes',
    seconds: 'Seconds',
    frequency: 'Announcement frequency',
    slow: 'Slow (7s)',
    normal: 'Normal (5s)',
    fast: 'Fast (3s)',
    double: 'Double',
    triple: 'Triple',
    skipRound: 'Skip to next round',
    skipBlock: 'Skip to next block',
    voiceProfile: 'Voice',
    trainingComplete: 'Training complete!',
    theme: 'Atmosphere',
    sport: 'Sport',
    exercise: 'Exercise',
    backToTraining: 'Back to training',
    noSavedWorkouts: 'No saved workouts',
    deleteConfirm: 'Delete this workout?',
    saveCurrentWorkout: 'Save this workout',
    createdOn: 'Created on',
    newName: 'New name',
    selectWorkout: 'Select a workout'
  },
  es: {
    title: 'Entrenamiento de Kickboxing',
    warmup: 'Calentamiento',
    jumpRope: 'Saltar la cuerda',
    strength: 'Musculación',
    heavyBag: 'Saco de boxeo',
    shadowBoxing: 'Shadow boxing',
    cooldown: 'Estiramiento/Recuperación',
    sparring: 'Sparring',
    start: 'Iniciar',
    pause: 'Pausa',
    reset: 'Reiniciar',
    round: 'Round',
    rest: 'Descanso',
    prepare: 'Preparación',
    work: 'Trabajo',
    settings: 'Ajustes',
    addBlock: 'Añadir bloque',
    duration: 'Duración',
    rounds: 'Rounds',
    workTime: 'Tiempo de trabajo',
    restTime: 'Tiempo de descanso',
    volume: 'Volumen',
    selectTechniques: 'Seleccionar técnicas',
    punches: 'Puñetazos',
    kicks: 'Patadas',
    knees: 'Rodillas',
    elbows: 'Codos',
    combos: 'Combos',
    selectExercises: 'Seleccionar ejercicios',
    reps: 'Repeticiones',
    speedUp: '¡Acelera!',
    normalPace: 'Ritmo normal',
    edit: 'Editar',
    save: 'Guardar',
    cancel: 'Cancelar',
    delete: 'Eliminar',
    duplicate: 'Duplicar',
    rename: 'Renombrar',
    language: 'Idioma',
    saveWorkout: 'Guardar entrenamiento',
    loadWorkout: 'Cargar',
    workoutName: 'Nombre del entrenamiento',
    myWorkouts: 'Mis entrenamientos',
    presetWorkouts: 'Sesiones',
    preset30min: 'Sesión 30 minutos',
    preset60min: 'Sesión 1 hora',
    preset90min: 'Sesión 1h30',
    minutes: 'Minutos',
    seconds: 'Segundos',
    frequency: 'Frecuencia de anuncios',
    slow: 'Lento (7s)',
    normal: 'Normal (5s)',
    fast: 'Rápido (3s)',
    double: 'Doble',
    triple: 'Triple',
    skipRound: 'Saltar al siguiente round',
    skipBlock: 'Saltar al siguiente bloque',
    voiceProfile: 'Voz',
    trainingComplete: '¡Entrenamiento completado!',
    theme: 'Ambiente',
    sport: 'Deporte',
    exercise: 'Ejercicio',
    backToTraining: 'Volver al entrenamiento',
    noSavedWorkouts: 'No hay entrenamientos guardados',
    deleteConfirm: '¿Eliminar este entrenamiento?',
    saveCurrentWorkout: 'Guardar este entrenamiento',
    createdOn: 'Creado el',
    newName: 'Nuevo nombre',
    selectWorkout: 'Seleccionar entrenamiento'
  }
};

// Fonction pour créer les séances préenregistrées
const createPresetWorkout = (duration) => {
  if (duration === 30) {
    return [
      { id: 'warmup', type: 'warmup', rounds: 2, workTime: 120, restTime: 30, frequency: 'normal' },
      { id: 'jumpRope', type: 'jumpRope', rounds: 2, workTime: 180, restTime: 60, frequency: 'normal' },
      { id: 'strength', type: 'strength', rounds: 2, exercises: { pushups: 15, squats: 20 } },
      { id: 'heavyBag', type: 'heavyBag', rounds: 3, workTime: 120, restTime: 60, techniques: ['punches', 'kicks', 'combos'], frequency: 'normal' },
      { id: 'shadowBoxing', type: 'shadowBoxing', rounds: 2, workTime: 60, restTime: 30, frequency: 'normal' },
      { id: 'cooldown', type: 'cooldown', rounds: 1, workTime: 60, restTime: 0, frequency: 'normal' }
    ];
  } else if (duration === 60) {
    return [
      { id: 'warmup', type: 'warmup', rounds: 2, workTime: 180, restTime: 60, frequency: 'normal' },
      { id: 'jumpRope', type: 'jumpRope', rounds: 4, workTime: 180, restTime: 60, frequency: 'normal' },
      { id: 'strength', type: 'strength', rounds: 3, exercises: { pushups: 20, squats: 25, burpees: 10 } },
      { id: 'heavyBag', type: 'heavyBag', rounds: 5, workTime: 180, restTime: 60, techniques: ['punches', 'kicks', 'knees', 'combos'], frequency: 'normal' },
      { id: 'shadowBoxing', type: 'shadowBoxing', rounds: 3, workTime: 120, restTime: 60, frequency: 'normal' },
      { id: 'cooldown', type: 'cooldown', rounds: 2, workTime: 60, restTime: 30, frequency: 'normal' }
    ];
  } else if (duration === 90) {
    return [
      { id: 'warmup', type: 'warmup', rounds: 3, workTime: 180, restTime: 60, frequency: 'normal' },
      { id: 'jumpRope', type: 'jumpRope', rounds: 6, workTime: 180, restTime: 60, frequency: 'normal' },
      { id: 'strength', type: 'strength', rounds: 4, exercises: { pushups: 25, squats: 30, burpees: 15, abs: 30 } },
      { id: 'heavyBag', type: 'heavyBag', rounds: 8, workTime: 180, restTime: 60, techniques: ['punches', 'kicks', 'knees', 'elbows', 'combos'], frequency: 'normal' },
      { id: 'shadowBoxing', type: 'shadowBoxing', rounds: 4, workTime: 120, restTime: 60, frequency: 'normal' },
      { id: 'cooldown', type: 'cooldown', rounds: 2, workTime: 90, restTime: 30, frequency: 'normal' }
    ];
  }
  return [];
};

// Fonction pour jouer la sonnerie de boxe
const playBellSound = () => {
  const audioContext = new (window.AudioContext || window.webkitAudioContext)();
  const oscillator = audioContext.createOscillator();
  const gainNode = audioContext.createGain();
  
  oscillator.connect(gainNode);
  gainNode.connect(audioContext.destination);
  
  oscillator.frequency.value = 800;
  oscillator.type = 'sine';
  
  gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
  gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
  
  oscillator.start(audioContext.currentTime);
  oscillator.stop(audioContext.currentTime + 0.5);
};

function KickboxingTrainer() {
  const [language, setLanguage] = useState('fr');
  const [blocks, setBlocks] = useState([]);
  const [currentBlockIndex, setCurrentBlockIndex] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [timeLeft, setTimeLeft] = useState(0);
  const [currentRound, setCurrentRound] = useState(1);
  const [isWorkPhase, setIsWorkPhase] = useState(true);
  const [volume, setVolume] = useState(0.7);
  const [editingBlock, setEditingBlock] = useState(null);
  const [showSettings, setShowSettings] = useState(false);
  const [savedWorkouts, setSavedWorkouts] = useState([]);
  const [workoutName, setWorkoutName] = useState('');
  const [showSaveDialog, setShowSaveDialog] = useState(false);
  const [draggedIndex, setDraggedIndex] = useState(null);
  const [voiceProfile, setVoiceProfile] = useState('default');
  const [trainingCompleted, setTrainingCompleted] = useState(false);
  const [theme, setTheme] = useState('muayThaiCamp');
  const [availableVoices, setAvailableVoices] = useState([]);
  const [showWorkoutsPage, setShowWorkoutsPage] = useState(false);
  const [renamingWorkout, setRenamingWorkout] = useState(null);
  const [newWorkoutName, setNewWorkoutName] = useState('');
  
  const timerRef = useRef(null);
  const lastAnnouncementRef = useRef(0);
  const lastJumpRopePaceChangeRef = useRef(0);
  const currentExerciseIndexRef = useRef(0);
  const currentRepRef = useRef(1);

  const t = TRANSLATIONS[language];
  const currentTheme = THEMES[theme];

  // Charger les voix disponibles du navigateur
  useEffect(() => {
    const loadVoices = () => {
      const voices = window.speechSynthesis.getVoices();
      setAvailableVoices(voices);
    };
    
    loadVoices();
    window.speechSynthesis.onvoiceschanged = loadVoices;
  }, []);

  // Charger les entraînements sauvegardés
  useEffect(() => {
    const loadSavedWorkouts = async () => {
      try {
        const result = await window.storage.list('workout:');
        if (result && result.keys) {
          const workouts = [];
          for (const key of result.keys) {
            const data = await window.storage.get(key);
            if (data && data.value) {
              workouts.push(JSON.parse(data.value));
            }
          }
          setSavedWorkouts(workouts);
        }
      } catch (error) {
        console.log('No saved workouts found');
      }
    };
    
    loadSavedWorkouts();
    
    if (blocks.length === 0) {
      setBlocks(createPresetWorkout(30));
    }
  }, []);

  // Fonction pour sélectionner la meilleure voix selon le profil et la langue
  const getVoiceForProfile = () => {
    if (availableVoices.length === 0) return null;
    
    const langCode = language === 'fr' ? 'fr' : language === 'es' ? 'es' : 'en';
    const langVoices = availableVoices.filter(v => v.lang.startsWith(langCode));
    
    if (langVoices.length === 0) return availableVoices[0];
    
    const profileVoiceMap = {
      gandalf: (voices) => {
        return voices.find(v => 
          v.name.toLowerCase().includes('male') && 
          !v.name.toLowerCase().includes('female')
        ) || voices[0];
      },
      dumbledore: (voices) => {
        return voices.find(v => 
          v.name.toLowerCase().includes('male') && 
          !v.name.toLowerCase().includes('female')
        ) || voices[0];
      },
      apolloCreed: (voices) => {
        return voices.find(v => 
          v.name.toLowerCase().includes('male') && 
          !v.name.toLowerCase().includes('female')
        ) || voices[0];
      },
      rocky: (voices) => {
        return voices.find(v => 
          v.name.toLowerCase().includes('male') && 
          !v.name.toLowerCase().includes('female')
        ) || voices[0];
      },
      default: (voices) => voices[0]
    };
    
    const selectVoice = profileVoiceMap[voiceProfile] || profileVoiceMap.default;
    return selectVoice(langVoices);
  };

  // Synthèse vocale améliorée - PAS de voix pour warmup, shadowBoxing, cooldown
  const speak = (text, shouldMultiply = false, isCombo = false, blockType = '') => {
    if (blockType === 'warmup' || blockType === 'shadowBoxing' || blockType === 'cooldown') {
      return;
    }
    
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      
      let finalText = text;
      
      const voiceParams = {
        gandalf: { pitch: 0.65, rate: 0.8 },
        dumbledore: { pitch: 0.7, rate: 0.85 },
        apolloCreed: { pitch: 1.2, rate: 1.2 },
        rocky: { pitch: 0.9, rate: 0.95 },
        default: { pitch: 1, rate: 1 }
      };
      
      const params = voiceParams[voiceProfile] || voiceParams.default;
      
      if (shouldMultiply && blockType === 'heavyBag' && !isCombo && Math.random() < 0.3) {
        const multiplier = Math.random() < 0.5 ? 2 : 3;
        const multiplierText = multiplier === 2 ? t.double : t.triple;
        finalText = `${multiplierText} ${text}`;
      }
      
      const utterance = new SpeechSynthesisUtterance(finalText);
      const selectedVoice = getVoiceForProfile();
      if (selectedVoice) {
        utterance.voice = selectedVoice;
      }
      utterance.lang = language === 'fr' ? 'fr-FR' : language === 'es' ? 'es-ES' : 'en-US';
      utterance.volume = volume;
      utterance.rate = params.rate;
      utterance.pitch = params.pitch;
      window.speechSynthesis.speak(utterance);
    }
  };

  // Logique du timer
  useEffect(() => {
    if (isRunning && timeLeft > 0) {
      timerRef.current = setTimeout(() => {
        setTimeLeft(timeLeft - 1);
        handleTimerLogic();
      }, 1000);
    } else if (timeLeft === 0 && isRunning) {
      handlePhaseComplete();
    }
    return () => clearTimeout(timerRef.current);
  }, [isRunning, timeLeft]);

  const handleTimerLogic = () => {
    const currentBlock = blocks[currentBlockIndex];
    const now = Date.now();
    
    const getFrequencyInterval = () => {
      const freq = currentBlock.frequency || 'normal';
      return freq === 'slow' ? 7000 : freq === 'fast' ? 3000 : 5000;
    };
    
    if (currentBlock.type === 'jumpRope' && isWorkPhase) {
      const minInterval = 20000;
      const maxInterval = 40000;
      const interval = minInterval + Math.random() * (maxInterval - minInterval);
      
      if (now - lastJumpRopePaceChangeRef.current > interval) {
        const messages = [t.speedUp, t.normalPace];
        const message = messages[Math.floor(Math.random() * messages.length)];
        speak(message, false, false, 'jumpRope');
        lastJumpRopePaceChangeRef.current = now;
      }
    } else if (currentBlock.type === 'heavyBag' && isWorkPhase) {
      const interval = getFrequencyInterval();
      
      if (now - lastAnnouncementRef.current > interval) {
        const selectedTechniques = currentBlock.techniques || [];
        const allTechniques = [];
        
        selectedTechniques.forEach(cat => {
          if (TECHNIQUES[language][cat]) {
            allTechniques.push(...TECHNIQUES[language][cat].map(t => ({ text: t, isCombo: cat === 'combos' })));
          }
        });
        
        if (allTechniques.length > 0) {
          const technique = allTechniques[Math.floor(Math.random() * allTechniques.length)];
          speak(technique.text, true, technique.isCombo, 'heavyBag');
          lastAnnouncementRef.current = now;
        }
      }
    } else if (currentBlock.type === 'sparring' && isWorkPhase) {
      const interval = getFrequencyInterval();
      
      if (now - lastAnnouncementRef.current > interval) {
        const motivationalMessages = {
          fr: ['Gardez votre garde !', 'Bougez !', 'Contre-attaquez !', 'Respirez !'],
          en: ['Keep your guard up!', 'Move!', 'Counter!', 'Breathe!'],
          es: ['¡Mantén la guardia!', '¡Muévete!', '¡Contraataca!', '¡Respira!']
        };
        
        const messages = motivationalMessages[language] || motivationalMessages.en;
        speak(messages[Math.floor(Math.random() * messages.length)], false, false, 'sparring');
        lastAnnouncementRef.current = now;
      }
    } else if (currentBlock.type === 'strength' && isWorkPhase) {
      const exercises = Object.entries(currentBlock.exercises || {});
      if (exercises.length > 0) {
        const [exerciseKey, reps] = exercises[currentExerciseIndexRef.current];
        
        if (currentRepRef.current <= reps) {
          speak(currentRepRef.current.toString(), false, false, 'strength');
          currentRepRef.current++;
        }
      }
    }

    if (timeLeft === 10 && isWorkPhase) {
      speak("10", false, false, currentBlock.type);
    } else if (timeLeft === 3) {
      playBellSound();
      speak("3", false, false, currentBlock.type);
    } else if (timeLeft === 2) {
      speak("2", false, false, currentBlock.type);
    } else if (timeLeft === 1) {
      speak("1", false, false, currentBlock.type);
    }
  };

  const handlePhaseComplete = () => {
    const currentBlock = blocks[currentBlockIndex];
    playBellSound();
    
    if (currentBlock.type === 'jumpRope' || currentBlock.type === 'heavyBag' || currentBlock.type === 'sparring' || currentBlock.type === 'shadowBoxing' || currentBlock.type === 'warmup' || currentBlock.type === 'cooldown') {
      if (isWorkPhase) {
        setIsWorkPhase(false);
        setTimeLeft(currentBlock.restTime);
        speak(t.rest, false, false, currentBlock.type);
      } else {
        if (currentRound < currentBlock.rounds) {
          setCurrentRound(currentRound + 1);
          setIsWorkPhase(true);
          setTimeLeft(currentBlock.workTime);
          speak(`${t.round} ${currentRound + 1}`, false, false, currentBlock.type);
        } else {
          goToNextBlock();
        }
      }
    } else if (currentBlock.type === 'strength') {
      const exercises = Object.entries(currentBlock.exercises || {});
      
      if (isWorkPhase) {
        if (currentRound < currentBlock.rounds) {
          setCurrentRound(currentRound + 1);
          setIsWorkPhase(false);
          setTimeLeft(currentBlock.restTime || 60);
          currentRepRef.current = 1;
          speak(t.rest, false, false, 'strength');
        } else {
          goToNextBlock();
        }
      } else {
        setIsWorkPhase(true);
        if (exercises.length > 0) {
          const exerciseIndex = (currentRound - 1) % exercises.length;
          const [exerciseKey, reps] = exercises[exerciseIndex];
          const exerciseName = EXERCISES[language][exerciseKey];
          setTimeLeft(Math.ceil(reps * 2));
          currentRepRef.current = 1;
          speak(`${t.exercise} ${currentRound} - ${exerciseName}`, false, false, 'strength');
        }
      }
    } else {
      goToNextBlock();
    }
  };

  const goToNextBlock = () => {
    if (currentBlockIndex < blocks.length - 1) {
      setCurrentBlockIndex(currentBlockIndex + 1);
      resetBlock(currentBlockIndex + 1);
    } else {
      setIsRunning(false);
      setTrainingCompleted(true);
      speak(t.trainingComplete, false, false, 'completion');
      
      setTimeout(() => {
        resetToInitialState();
      }, 3000);
    }
  };

  const resetToInitialState = () => {
    setCurrentBlockIndex(0);
    setIsRunning(false);
    setTimeLeft(0);
    setCurrentRound(1);
    setIsWorkPhase(true);
    currentExerciseIndexRef.current = 0;
    currentRepRef.current = 1;
    setTrainingCompleted(false);
    
    if (blocks.length > 0) {
      const firstBlock = blocks[0];
      if (firstBlock.type === 'jumpRope' || firstBlock.type === 'heavyBag' || firstBlock.type === 'sparring' || firstBlock.type === 'shadowBoxing' || firstBlock.type === 'warmup' || firstBlock.type === 'cooldown') {
        setTimeLeft(firstBlock.workTime);
      } else if (firstBlock.type === 'strength') {
        const exercises = Object.entries(firstBlock.exercises || {});
        if (exercises.length > 0) {
          const [exerciseKey, reps] = exercises[0];
          setTimeLeft(Math.ceil(reps * 2));
        }
      }
    }
  };

  const resetBlock = (blockIndex) => {
    const block = blocks[blockIndex];
    setCurrentRound(1);
    setIsWorkPhase(true);
    currentExerciseIndexRef.current = 0;
    currentRepRef.current = 1;
    
    if (block.type === 'jumpRope' || block.type === 'heavyBag' || block.type === 'sparring' || block.type === 'shadowBoxing' || block.type === 'warmup' || block.type === 'cooldown') {
      setTimeLeft(block.workTime);
    } else if (block.type === 'strength') {
      const exercises = Object.entries(block.exercises || {});
      if (exercises.length > 0) {
        const [exerciseKey, reps] = exercises[0];
        setTimeLeft(Math.ceil(reps * 2));
      }
    }
    
    const blockName = t[block.type] || block.type;
    speak(blockName, false, false, block.type);
  };

  const startTraining = () => {
    if (!isRunning && blocks.length > 0) {
      setIsRunning(true);
      setTrainingCompleted(false);
      if (timeLeft === 0) {
        resetBlock(currentBlockIndex);
      }
    }
  };

  const skipToNextRound = () => {
    const currentBlock = blocks[currentBlockIndex];
    
    if (currentBlock.rounds && currentRound < currentBlock.rounds) {
      setCurrentRound(currentRound + 1);
      setIsWorkPhase(true);
      
      if (currentBlock.type === 'strength') {
        currentRepRef.current = 1;
        const exercises = Object.entries(currentBlock.exercises || {});
        if (exercises.length > 0) {
          const exerciseIndex = (currentRound) % exercises.length;
          const [exerciseKey, reps] = exercises[exerciseIndex];
          const exerciseName = EXERCISES[language][exerciseKey];
          setTimeLeft(Math.ceil(reps * 2));
          speak(`${t.exercise} ${currentRound + 1} - ${exerciseName}`, false, false, 'strength');
        }
      } else {
        setTimeLeft(currentBlock.workTime);
        speak(`${t.round} ${currentRound + 1}`, false, false, currentBlock.type);
      }
      playBellSound();
    } else {
      skipToNextBlock();
    }
  };

  const skipToNextBlock = () => {
    playBellSound();
    goToNextBlock();
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleDragStart = (index) => {
    setDraggedIndex(index);
  };

  const handleDragOver = (e, index) => {
    e.preventDefault();
    if (draggedIndex === null || draggedIndex === index) return;
    
    const newBlocks = [...blocks];
    const draggedBlock = newBlocks[draggedIndex];
    newBlocks.splice(draggedIndex, 1);
    newBlocks.splice(index, 0, draggedBlock);
    
    setBlocks(newBlocks);
    setDraggedIndex(index);
  };

  const handleDragEnd = () => {
    setDraggedIndex(null);
  };

  const deleteBlock = (index) => {
    setBlocks(blocks.filter((_, i) => i !== index));
  };

  const duplicateBlock = (index) => {
    const blockToDuplicate = { ...blocks[index], id: `${blocks[index].type}-${Date.now()}` };
    const newBlocks = [...blocks];
    newBlocks.splice(index + 1, 0, blockToDuplicate);
    setBlocks(newBlocks);
  };

  const updateBlock = (index, updates) => {
    const newBlocks = [...blocks];
    newBlocks[index] = { ...newBlocks[index], ...updates };
    setBlocks(newBlocks);
  };

  const addBlock = (type) => {
    const newBlock = {
      id: `${type}-${Date.now()}`,
      type,
      frequency: 'normal',
      ...(type === 'jumpRope' ? { rounds: 3, workTime: 180, restTime: 60 } : {}),
      ...(type === 'heavyBag' ? { rounds: 3, workTime: 180, restTime: 60, techniques: ['punches', 'kicks'] } : {}),
      ...(type === 'strength' ? { rounds: 3, exercises: { pushups: 15, squats: 20, abs: 25 }, restTime: 60 } : {}),
      ...(type === 'warmup' || type === 'shadowBoxing' || type === 'cooldown' ? { rounds: 2, workTime: 120, restTime: 30 } : {}),
      ...(type === 'sparring' ? { rounds: 5, workTime: 180, restTime: 60, sport: 'kickboxing' } : {})
    };
    setBlocks([...blocks, newBlock]);
  };

  const saveWorkout = async () => {
    if (!workoutName.trim()) {
      alert(language === 'fr' ? 'Veuillez entrer un nom' : language === 'es' ? 'Ingrese un nombre' : 'Please enter a name');
      return;
    }
    
    const workout = {
      name: workoutName,
      blocks: blocks,
      createdAt: new Date().toISOString()
    };
    
    try {
      await window.storage.set(`workout:${workoutName}`, JSON.stringify(workout));
      const updatedWorkouts = [...savedWorkouts.filter(w => w.name !== workoutName), workout];
      setSavedWorkouts(updatedWorkouts);
      setWorkoutName('');
      setShowSaveDialog(false);
      alert(t.saveWorkout + ' ✓');
    } catch (error) {
      console.error('Error saving workout:', error);
    }
  };

  const loadWorkout = async (name) => {
    try {
      const result = await window.storage.get(`workout:${name}`);
      if (result && result.value) {
        const workout = JSON.parse(result.value);
        setBlocks(workout.blocks);
        resetToInitialState();
        setShowWorkoutsPage(false);
      }
    } catch (error) {
      console.error('Error loading workout:', error);
    }
  };

  const deleteWorkout = async (name) => {
    if (!confirm(t.deleteConfirm)) return;
    
    try {
      await window.storage.delete(`workout:${name}`);
      setSavedWorkouts(savedWorkouts.filter(w => w.name !== name));
    } catch (error) {
      console.error('Error deleting workout:', error);
    }
  };

  const renameWorkout = async (oldName, newName) => {
    if (!newName.trim() || newName === oldName) {
      setRenamingWorkout(null);
      return;
    }
    
    try {
      const result = await window.storage.get(`workout:${oldName}`);
      if (result && result.value) {
        const workout = JSON.parse(result.value);
        workout.name = newName;
        
        await window.storage.delete(`workout:${oldName}`);
        await window.storage.set(`workout:${newName}`, JSON.stringify(workout));
        
        const updatedWorkouts = savedWorkouts.map(w => w.name === oldName ? workout : w);
        setSavedWorkouts(updatedWorkouts);
        setRenamingWorkout(null);
        setNewWorkoutName('');
      }
    } catch (error) {
      console.error('Error renaming workout:', error);
    }
  };

  const loadPreset = (duration) => {
    setBlocks(createPresetWorkout(duration));
    resetToInitialState();
  };

  const currentBlock = blocks[currentBlockIndex];

  // Page "Mes entraînements"
  if (showWorkoutsPage) {
    return (
      <div className={`min-h-screen text-white font-sans`} style={{ background: currentTheme.backgroundImage, backgroundSize: 'cover', backgroundAttachment: 'fixed' }}>
        <div className="min-h-screen backdrop-blur-sm" style={{ backgroundColor: 'rgba(0,0,0,0.3)' }}>
          <header className="bg-black/50 backdrop-blur-md border-b border-white/10 sticky top-0 z-50">
            <div className="container mx-auto px-4 py-4 flex justify-between items-center">
              <h1 className="title-font text-4xl md:text-5xl tracking-wider" style={{ color: currentTheme.colors.primary }}>
                {t.myWorkouts}
              </h1>
              <button
                onClick={() => setShowWorkoutsPage(false)}
                className="flex items-center gap-2 px-6 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
                {t.backToTraining}
              </button>
            </div>
          </header>

          <div className="container mx-auto px-4 py-8">
            {savedWorkouts.length === 0 ? (
              <div className="text-center py-20">
                <List className="w-20 h-20 mx-auto mb-6 opacity-50" />
                <h2 className="text-3xl font-bold mb-4">{t.noSavedWorkouts}</h2>
                <p className="text-gray-400 mb-8">Créez votre premier entraînement et sauvegardez-le !</p>
                <button
                  onClick={() => setShowWorkoutsPage(false)}
                  className="px-8 py-4 rounded-xl font-bold transition-all"
                  style={{ backgroundColor: currentTheme.colors.primary }}
                >
                  {t.backToTraining}
                </button>
              </div>
            ) : (
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {savedWorkouts.map(workout => (
                  <div key={workout.name} className="bg-black/60 backdrop-blur-lg rounded-xl p-6 border-2 hover:shadow-2xl transition-all" style={{ borderColor: currentTheme.colors.primary + '50' }}>
                    {renamingWorkout === workout.name ? (
                      <div className="mb-4">
                        <input
                          type="text"
                          value={newWorkoutName}
                          onChange={(e) => setNewWorkoutName(e.target.value)}
                          onKeyPress={(e) => e.key === 'Enter' && renameWorkout(workout.name, newWorkoutName)}
                          className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 mb-2"
                          autoFocus
                        />
                        <div className="flex gap-2">
                          <button
                            onClick={() => renameWorkout(workout.name, newWorkoutName)}
                            className="flex-1 px-3 py-2 bg-green-600 hover:bg-green-700 rounded text-sm"
                          >
                            {t.save}
                          </button>
                          <button
                            onClick={() => {
                              setRenamingWorkout(null);
                              setNewWorkoutName('');
                            }}
                            className="flex-1 px-3 py-2 bg-gray-600 hover:bg-gray-700 rounded text-sm"
                          >
                            {t.cancel}
                          </button>
                        </div>
                      </div>
                    ) : (
                      <h3 className="text-2xl font-bold mb-3" style={{ color: currentTheme.colors.secondary }}>{workout.name}</h3>
                    )}
                    <p className="text-sm text-gray-400 mb-4">
                      {t.createdOn}: {new Date(workout.createdAt).toLocaleDateString(language)}
                    </p>
                    <p className="text-sm text-gray-300 mb-6">
                      {workout.blocks.length} blocs d'entraînement
                    </p>
                    <div className="flex gap-2">
                      <button
                        onClick={() => loadWorkout(workout.name)}
                        className="flex-1 px-4 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-bold transition-colors flex items-center justify-center gap-2"
                      >
                        <Upload className="w-4 h-4" />
                        {t.loadWorkout}
                      </button>
                      <button
                        onClick={() => {
                          setRenamingWorkout(workout.name);
                          setNewWorkoutName(workout.name);
                        }}
                        className="p-3 bg-yellow-600/80 hover:bg-yellow-600 rounded-lg transition-colors"
                        title={t.rename}
                      >
                        <Pencil className="w-5 h-5" />
                      </button>
                      <button
                        onClick={() => deleteWorkout(workout.name)}
                        className="p-3 bg-red-600/80 hover:bg-red-600 rounded-lg transition-colors"
                      >
                        <Trash2 className="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  // Page principale d'entraînement
  return (
    <div className={`min-h-screen text-white font-sans`} style={{ background: currentTheme.backgroundImage, backgroundSize: 'cover', backgroundAttachment: 'fixed' }}>
      <div className="min-h-screen backdrop-blur-sm" style={{ backgroundColor: 'rgba(0,0,0,0.3)' }}>
        <style>{`
          @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Oswald:wght@400;600;700&display=swap');
          
          body {
            font-family: 'Oswald', sans-serif;
          }
          
          .title-font {
            font-family: 'Bebas Neue', cursive;
          }
          
          @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 0 20px ${currentTheme.colors.primary}80; }
            50% { box-shadow: 0 0 40px ${currentTheme.colors.primary}; }
          }
          
          .pulse-glow {
            animation: pulse-glow 2s ease-in-out infinite;
          }
          
          @keyframes slide-in {
            from { transform: translateY(-20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
          }
          
          .slide-in {
            animation: slide-in 0.5s ease-out;
          }
          
          @keyframes celebration {
            0%, 100% { transform: scale(1) rotate(0deg); }
            25% { transform: scale(1.1) rotate(-5deg); }
            75% { transform: scale(1.1) rotate(5deg); }
          }
          
          .celebration {
            animation: celebration 1s ease-in-out infinite;
          }
          
          .timer-ring {
            stroke-dasharray: 440;
            stroke-dashoffset: 440;
            transform: rotate(-90deg);
            transform-origin: center;
            transition: stroke-dashoffset 1s linear;
          }
          
          .block-card {
            background: ${currentTheme.colors.cardBg};
            backdrop-filter: blur(10px);
            border: 2px solid ${currentTheme.colors.primary}30;
            transition: all 0.3s ease;
            cursor: grab;
          }
          
          .block-card:active {
            cursor: grabbing;
          }
          
          .block-card:hover {
            border-color: ${currentTheme.colors.primary}80;
            transform: translateY(-2px);
            box-shadow: 0 8px 16px ${currentTheme.colors.primary}20;
          }
          
          .active-block {
            border: 3px solid ${currentTheme.colors.primary};
            box-shadow: 0 0 30px ${currentTheme.colors.primary}60;
          }
          
          .dragging {
            opacity: 0.5;
          }
        `}</style>

        {/* Header */}
        <header className="bg-black/50 backdrop-blur-md border-b border-white/10 sticky top-0 z-50">
          <div className="container mx-auto px-4 py-4 flex justify-between items-center flex-wrap gap-4">
            <h1 className="title-font text-4xl md:text-5xl tracking-wider" style={{ color: currentTheme.colors.primary }}>{t.title}</h1>
            
            <div className="flex items-center gap-3 flex-wrap">
              {/* Ambiance */}
              <div className="flex flex-col">
                <label className="text-xs text-gray-400 mb-1">{t.theme}</label>
                <select 
                  value={theme}
                  onChange={(e) => setTheme(e.target.value)}
                  className="bg-gray-800/80 border border-white/20 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-white/50"
                >
                  {Object.entries(THEMES).map(([key, themeData]) => (
                    <option key={key} value={key}>{themeData.name[language]}</option>
                  ))}
                </select>
              </div>

              {/* Séances */}
              <div className="flex flex-col">
                <label className="text-xs text-gray-400 mb-1">{t.presetWorkouts}</label>
                <select 
                  onChange={(e) => e.target.value && loadPreset(parseInt(e.target.value))}
                  className="bg-gray-800/80 border border-white/20 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-white/50"
                  defaultValue=""
                >
                  <option value="" disabled>{t.presetWorkouts}</option>
                  <option value="30">{t.preset30min}</option>
                  <option value="60">{t.preset60min}</option>
                  <option value="90">{t.preset90min}</option>
                </select>
              </div>

              {/* Mes entraînements */}
              <div className="flex flex-col">
                <label className="text-xs text-gray-400 mb-1">{t.myWorkouts}</label>
                <select 
                  onChange={(e) => {
                    if (e.target.value === '__view_all__') {
                      setShowWorkoutsPage(true);
                    } else if (e.target.value) {
                      loadWorkout(e.target.value);
                    }
                    e.target.value = '';
                  }}
                  className="bg-gray-800/80 border border-white/20 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-white/50"
                  defaultValue=""
                >
                  <option value="" disabled>{t.selectWorkout}</option>
                  <option value="__view_all__">📋 {t.myWorkouts}</option>
                  <option disabled>────────</option>
                  {savedWorkouts.map(workout => (
                    <option key={workout.name} value={workout.name}>{workout.name}</option>
                  ))}
                </select>
              </div>

              {/* Voix */}
              <div className="flex flex-col">
                <label className="text-xs text-gray-400 mb-1">{t.voiceProfile}</label>
                <select 
                  value={voiceProfile}
                  onChange={(e) => setVoiceProfile(e.target.value)}
                  className="bg-gray-800/80 border border-purple-500/30 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-purple-500"
                >
                  <option value="default">🎤 Normal</option>
                  <option value="gandalf">🧙 Gandalf</option>
                  <option value="dumbledore">🪄 Dumbledore</option>
                  <option value="apolloCreed">🥊 Apollo Creed</option>
                  <option value="rocky">🥊 Rocky</option>
                </select>
              </div>

              <select 
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="bg-gray-800/80 border border-white/20 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-white/50"
              >
                <option value="fr">🇫🇷</option>
                <option value="en">🇬🇧</option>
                <option value="es">🇪🇸</option>
              </select>

              <button
                onClick={() => setShowSettings(!showSettings)}
                className="p-2 rounded-lg transition-colors"
                style={{ backgroundColor: currentTheme.colors.primary }}
              >
                <Settings className="w-5 h-5" />
              </button>
            </div>
          </div>
        </header>

        {/* Dialog de sauvegarde */}
        {showSaveDialog && (
          <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
            <div className="bg-gray-900 rounded-xl p-6 max-w-md w-full border-2" style={{ borderColor: currentTheme.colors.primary }}>
              <h3 className="text-2xl font-bold mb-4" style={{ color: currentTheme.colors.primary }}>{t.saveWorkout}</h3>
              <input
                type="text"
                value={workoutName}
                onChange={(e) => setWorkoutName(e.target.value)}
                placeholder={t.workoutName}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 mb-4 focus:outline-none focus:border-white"
              />
              <div className="flex gap-3">
                <button
                  onClick={saveWorkout}
                  className="flex-1 px-6 py-3 bg-green-600 hover:bg-green-700 rounded-lg font-bold transition-colors"
                >
                  {t.save}
                </button>
                <button
                  onClick={() => setShowSaveDialog(false)}
                  className="flex-1 px-6 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg font-bold transition-colors"
                >
                  {t.cancel}
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="container mx-auto px-4 py-8">
          {trainingCompleted && (
            <div className="mb-8 bg-green-600/90 backdrop-blur-lg rounded-2xl p-8 border-2 border-green-400 text-center celebration">
              <h2 className="title-font text-4xl md:text-5xl mb-4">🏆 {t.trainingComplete} 🏆</h2>
            </div>
          )}

          {currentBlock && !trainingCompleted && (
            <div className="mb-8 bg-black/60 backdrop-blur-lg rounded-2xl p-8 border-2 slide-in" style={{ borderColor: currentTheme.colors.primary + '50' }}>
              <div className="flex flex-col items-center">
                <h2 className="title-font text-3xl md:text-4xl mb-6" style={{ color: currentTheme.colors.secondary }}>
                  {t[currentBlock.type]}
                </h2>
                
                <div className="relative w-64 h-64 mb-6">
                  <svg className="w-full h-full" viewBox="0 0 160 160">
                    <circle cx="80" cy="80" r="70" fill="none" stroke={currentTheme.colors.primary + '40'} strokeWidth="8"/>
                    <circle 
                      cx="80" cy="80" r="70" 
                      fill="none" 
                      stroke={currentTheme.colors.primary}
                      strokeWidth="8"
                      className="timer-ring"
                      style={{
                        strokeDashoffset: (currentBlock.type === 'jumpRope' || currentBlock.type === 'heavyBag' || currentBlock.type === 'sparring' || currentBlock.type === 'shadowBoxing' || currentBlock.type === 'warmup' || currentBlock.type === 'cooldown')
                          ? 440 - (440 * timeLeft / (isWorkPhase ? currentBlock.workTime : currentBlock.restTime))
                          : 440 - (440 * timeLeft / 180)
                      }}
                    />
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <div className="title-font text-6xl md:text-7xl text-white pulse-glow">
                      {formatTime(timeLeft)}
                    </div>
                    {currentBlock.rounds && (
                      <div className="text-lg mt-2" style={{ color: currentTheme.colors.secondary }}>
                        {t.round} {currentRound}/{currentBlock.rounds}
                      </div>
                    )}
                    <div className="text-sm mt-1 text-gray-400">
                      {isWorkPhase ? t.work : t.rest}
                    </div>
                  </div>
                </div>

                <div className="flex gap-3 flex-wrap justify-center mb-4">
                  <button
                    onClick={isRunning ? () => setIsRunning(false) : startTraining}
                    className="flex items-center gap-2 px-8 py-4 rounded-xl text-xl font-bold transition-all transform hover:scale-105"
                    style={{ backgroundColor: currentTheme.colors.primary }}
                  >
                    {isRunning ? <><Pause className="w-6 h-6" /> {t.pause}</> : <><Play className="w-6 h-6" /> {t.start}</>}
                  </button>
                  <button
                    onClick={resetToInitialState}
                    className="flex items-center gap-2 px-8 py-4 bg-gray-700 hover:bg-gray-600 rounded-xl text-xl font-bold transition-all"
                  >
                    <RotateCcw className="w-6 h-6" /> {t.reset}
                  </button>
                </div>

                {isRunning && (
                  <div className="flex gap-3 mb-4">
                    <button
                      onClick={skipToNextRound}
                      className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-bold transition-all"
                    >
                      <SkipForward className="w-5 h-5" /> {t.skipRound}
                    </button>
                    <button
                      onClick={skipToNextBlock}
                      className="flex items-center gap-2 px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-bold transition-all"
                    >
                      <ChevronsRight className="w-5 h-5" /> {t.skipBlock}
                    </button>
                  </div>
                )}

                <div className="mt-6 w-full max-w-md">
                  <div className="flex items-center gap-4">
                    <Volume2 className="w-5 h-5" style={{ color: currentTheme.colors.secondary }} />
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.1"
                      value={volume}
                      onChange={(e) => setVolume(parseFloat(e.target.value))}
                      className="flex-1 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                      style={{ accentColor: currentTheme.colors.primary }}
                    />
                    <span className="text-sm w-12 text-right">{Math.round(volume * 100)}%</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Liste des blocs */}
          <div className="grid gap-4">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-2xl font-bold" style={{ color: currentTheme.colors.secondary }}>Programme d'entraînement</h3>
              {showSettings && (
                <div className="flex gap-2 flex-wrap">
                  {['warmup', 'jumpRope', 'strength', 'heavyBag', 'shadowBoxing', 'sparring', 'cooldown'].map(type => (
                    <button
                      key={type}
                      onClick={() => addBlock(type)}
                      className="px-4 py-2 rounded-lg text-sm transition-colors hover:opacity-80"
                      style={{ backgroundColor: currentTheme.colors.primary + 'CC' }}
                    >
                      <Plus className="w-4 h-4 inline mr-1" />
                      {t[type]}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {blocks.map((block, index) => (
              <div
                key={block.id}
                draggable
                onDragStart={() => handleDragStart(index)}
                onDragOver={(e) => handleDragOver(e, index)}
                onDragEnd={handleDragEnd}
                className={`block-card rounded-xl p-6 ${index === currentBlockIndex && isRunning ? 'active-block' : ''} ${draggedIndex === index ? 'dragging' : ''}`}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <GripVertical className="w-6 h-6 text-gray-400" />
                    <div>
                      <h4 className="text-xl font-bold" style={{ color: currentTheme.colors.secondary }}>{t[block.type]}</h4>
                      <p className="text-sm text-gray-400">
                        {block.rounds ? `${block.rounds} ${t.rounds}` : ''}
                        {block.type === 'sparring' && block.sport && ` - ${SPARRING_CONFIGS[block.sport].name[language]}`}
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={() => duplicateBlock(index)}
                      className="p-2 bg-blue-600 hover:bg-blue-700 rounded-lg"
                      title={t.duplicate}
                    >
                      <Copy className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => setEditingBlock(editingBlock === index ? null : index)}
                      className="p-2 bg-gray-700 hover:bg-gray-600 rounded-lg"
                    >
                      {editingBlock === index ? <X className="w-4 h-4" /> : <Edit2 className="w-4 h-4" />}
                    </button>
                    <button
                      onClick={() => deleteBlock(index)}
                      className="p-2 bg-red-600/80 hover:bg-red-600 rounded-lg"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {editingBlock === index && (
                  <div className="mt-4 p-4 bg-black/40 rounded-lg space-y-4">
                    {block.type === 'sparring' && (
                      <div>
                        <label className="block text-sm mb-2">{t.sport}</label>
                        <select
                          value={block.sport || 'kickboxing'}
                          onChange={(e) => {
                            const config = SPARRING_CONFIGS[e.target.value];
                            updateBlock(index, {
                              sport: e.target.value,
                              rounds: config.rounds,
                              workTime: config.workTime,
                              restTime: config.restTime
                            });
                          }}
                          className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2"
                        >
                          {Object.entries(SPARRING_CONFIGS).map(([key, config]) => (
                            <option key={key} value={key}>{config.name[language]}</option>
                          ))}
                        </select>
                      </div>
                    )}

                    {(block.type === 'jumpRope' || block.type === 'heavyBag' || block.type === 'sparring' || block.type === 'shadowBoxing' || block.type === 'warmup' || block.type === 'cooldown') && (
                      <>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          <div>
                            <label className="block text-sm mb-2">{t.rounds}</label>
                            <input
                              type="number"
                              value={block.rounds}
                              min="1"
                              max="20"
                              onChange={(e) => updateBlock(index, { rounds: parseInt(e.target.value) || 1 })}
                              className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2"
                            />
                          </div>
                          <div>
                            <label className="block text-sm mb-2">{t.workTime}</label>
                            <div className="flex gap-2">
                              <input
                                type="number"
                                value={Math.floor(block.workTime / 60)}
                                min="0"
                                max="10"
                                onChange={(e) => {
                                  const mins = parseInt(e.target.value) || 0;
                                  const secs = block.workTime % 60;
                                  updateBlock(index, { workTime: mins * 60 + secs });
                                }}
                                className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2"
                                placeholder="min"
                              />
                              <select
                                value={block.workTime % 60}
                                onChange={(e) => {
                                  const mins = Math.floor(block.workTime / 60);
                                  const secs = parseInt(e.target.value);
                                  updateBlock(index, { workTime: mins * 60 + secs });
                                }}
                                className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2"
                              >
                                {[0, 10, 20, 30, 40, 50].map(s => (
                                  <option key={s} value={s}>{s}s</option>
                                ))}
                              </select>
                            </div>
                          </div>
                          <div>
                            <label className="block text-sm mb-2">{t.restTime}</label>
                            <div className="flex gap-2">
                              <input
                                type="number"
                                value={Math.floor(block.restTime / 60)}
                                min="0"
                                max="10"
                                onChange={(e) => {
                                  const mins = parseInt(e.target.value) || 0;
                                  const secs = block.restTime % 60;
                                  updateBlock(index, { restTime: mins * 60 + secs });
                                }}
                                className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2"
                                placeholder="min"
                              />
                              <select
                                value={block.restTime % 60}
                                onChange={(e) => {
                                  const mins = Math.floor(block.restTime / 60);
                                  const secs = parseInt(e.target.value);
                                  updateBlock(index, { restTime: mins * 60 + secs });
                                }}
                                className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2"
                              >
                                {[0, 10, 20, 30, 40, 50].map(s => (
                                  <option key={s} value={s}>{s}s</option>
                                ))}
                              </select>
                            </div>
                          </div>
                        </div>

                        <div>
                          <label className="block text-sm mb-2">{t.frequency}</label>
                          <select
                            value={block.frequency || 'normal'}
                            onChange={(e) => updateBlock(index, { frequency: e.target.value })}
                            className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2"
                          >
                            <option value="slow">{t.slow}</option>
                            <option value="normal">{t.normal}</option>
                            <option value="fast">{t.fast}</option>
                          </select>
                        </div>
                      </>
                    )}

                    {block.type === 'strength' && (
                      <>
                        <div>
                          <label className="block text-sm mb-2">{t.rounds} ({t.exercise}s)</label>
                          <input
                            type="number"
                            value={block.rounds}
                            min="1"
                            max="10"
                            onChange={(e) => updateBlock(index, { rounds: parseInt(e.target.value) || 1 })}
                            className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2"
                          />
                        </div>
                        <div>
                          <label className="block text-sm mb-2">{t.restTime} (entre exercices)</label>
                          <input
                            type="number"
                            value={block.restTime || 60}
                            min="0"
                            max="300"
                            onChange={(e) => updateBlock(index, { restTime: parseInt(e.target.value) || 60 })}
                            className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2"
                          />
                        </div>
                      </>
                    )}

                    {block.type === 'heavyBag' && (
                      <div>
                        <label className="block text-sm mb-2">{t.selectTechniques}</label>
                        <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
                          {['punches', 'kicks', 'knees', 'elbows', 'combos'].map(tech => (
                            <label key={tech} className="flex items-center gap-2 p-2 bg-gray-800 rounded cursor-pointer hover:bg-gray-700">
                              <input
                                type="checkbox"
                                checked={(block.techniques || []).includes(tech)}
                                onChange={(e) => {
                                  const techniques = block.techniques || [];
                                  if (e.target.checked) {
                                    updateBlock(index, { techniques: [...techniques, tech] });
                                  } else {
                                    updateBlock(index, { techniques: techniques.filter(t => t !== tech) });
                                  }
                                }}
                                style={{ accentColor: currentTheme.colors.primary }}
                              />
                              <span className="text-sm">{t[tech]}</span>
                            </label>
                          ))}
                        </div>
                      </div>
                    )}

                    {block.type === 'strength' && (
                      <div>
                        <label className="block text-sm mb-2">{t.selectExercises}</label>
                        <div className="space-y-2">
                          {Object.keys(EXERCISES[language]).map(ex => (
                            <div key={ex} className="flex items-center gap-3">
                              <input
                                type="checkbox"
                                checked={block.exercises && ex in block.exercises}
                                onChange={(e) => {
                                  const exercises = { ...block.exercises };
                                  if (e.target.checked) {
                                    exercises[ex] = 15;
                                  } else {
                                    delete exercises[ex];
                                  }
                                  updateBlock(index, { exercises });
                                }}
                                style={{ accentColor: currentTheme.colors.primary }}
                              />
                              <label className="flex-1">{EXERCISES[language][ex]}</label>
                              {block.exercises && ex in block.exercises && (
                                <input
                                  type="number"
                                  value={block.exercises[ex]}
                                  min="1"
                                  max="100"
                                  onChange={(e) => updateBlock(index, { 
                                    exercises: { ...block.exercises, [ex]: parseInt(e.target.value) || 1 }
                                  })}
                                  className="w-20 bg-gray-800 border border-gray-700 rounded px-2 py-1"
                                  placeholder={t.reps}
                                />
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Bouton de sauvegarde en bas de page */}
          <div className="mt-8 flex justify-center">
            <button
              onClick={() => setShowSaveDialog(true)}
              className="px-8 py-4 rounded-xl font-bold transition-all transform hover:scale-105 flex items-center gap-3"
              style={{ backgroundColor: currentTheme.colors.secondary }}
            >
              <Save className="w-6 h-6" />
              {t.saveCurrentWorkout}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default KickboxingTrainer;