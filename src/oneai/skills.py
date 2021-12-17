from dataclasses import dataclass

from oneai.classes import skillclass

@skillclass(name='summarize', iswriting=True, param_fields=['min_length', 'max_length'])
@dataclass
class Summarize:
    min_length: int = 5
    max_length: int = 100

@skillclass(name='entities')
class EntityDetection: pass

@skillclass(name='keywords')
class KeywordDetection: pass

@skillclass(name='highlights')
class Highlighting: pass

@skillclass(name='enhance', iswriting=True)
class EnhanceTranscription: pass