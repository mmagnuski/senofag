## EXPERIMENT STRUCTURE
### MAIN PROCEDURE
category | value
---|---
| COLORS  | 4  |
| TRIALS (per color)  | 160 |
| TRIALS (overall)  | 640 |
| BREAKS  | 10%  |
| TIME (in minutes) | 62.597  |

### PRIME DETECTION TASK
No effect circle nor SoA assessment.

category | value
---|---
| COLORS  | 0 (no circles) |
| TRIALS (per block)  | 72 |
| TRIALS (overall)  | 288 |
| BREAKS  | 10%  |
| TIME (in minutes) | 14.045  |

## BLOCK STRUCTURE
`response_hand` (2: left, right) * `condition` (2: comp, incomp) *  
`choice_type` (2: free, cued) * `target_position` (2: above, below)  
 = 16 base trials (8 free, 8 cued)  
(8 free, 8 cued) * proportion of [10 times free, 10 times cued] =  
80 + 80 = 160 trials per block  

## EXPERIMENT TIMELINE
one frame == 10 ms

| TIMELINE  | ms  |
|---|---|
|Fixation   | 1000-1500  |
| Prime  | 20  |
| Fixation  | 40  |
| Mask/Target  | 250  |
| Response  | max 1200  |
| Jittered delay  | 400-600  |
| Outcome  |  250 |
| Jittered delay  | 750-1250  |
| Agency rating  | max 1500  |
| CLEAR SCREEN  | 250-750  |
| SUM (avg)  | 5335|

## Markers:

code | meaning
---|---
 `1` | prime  
 `2` | target  
 `4` | effect  
 `8` | response  
 `16` | rating scale onset  
 `100` | fixation
 `101` | fixation response win (prime detection procedure)

## Lab monitor

 key | value  
---|---
LCD size (inch) | `24`
Aspect ratio | `16:9`
max resolution | `1920 x 1080` at 144Hz (DVI-DL)
Display area (mm) | `531.36 x 298.89`
Pixel pitch (mm) | `0.276`
Typ. brightness (cd/㎡) | `350`
Typ. contrast | `1000:1`
Typ. DCR (DyNomic Contrast Ratio) | `12M:1`
Panel type | `TN`
Response time | `1 ms` (GtG)

ja używam mniej więcej tak:
```python
from psychopy.monitors import Monitor

participant_distance = 80
monitor = "testMonitor"
if exp['in lab']:
    monitor = Monitor('BenQ', width=53.136, distance=participant_distance)
    monitor.setSizePix((1920, 1080))
```
