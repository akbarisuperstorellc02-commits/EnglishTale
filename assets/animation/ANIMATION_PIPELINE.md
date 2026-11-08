# EnglishTale — Character Animation Pipeline

## Added vector rigs
- `leo-idle-talk.svg`: blue hoodie, idle bob, periodic blink, mouth movement.
- `emma-idle-talk.svg`: pink sweater, idle bob, periodic blink, mouth movement.
- `ollie-idle-flap.svg`: owl guide, idle bob, periodic blink, wing flap, beak movement.

## Technical format
All assets are self-contained SVG with embedded CSS keyframes. They are resolution-independent and can be rendered by Chromium-based browsers. For video editing, render each SVG to PNG sequences or record the SVG animation at the required frame rate and composite it over scene backgrounds.

## Recommended episode timing
| Shot | Approx. duration | Character action |
|---|---:|---|
| Airport arrival | 45 s | Leo looks around; Emma greets him; Ollie introduces the lesson |
| Check-in | 85 s | Leo speaks to the check-in agent; Emma points to passport and ticket |
| Security | 70 s | Ollie flaps while explaining the security instruction |
| Departure gate | 80 s | Emma points at the gate display; Leo asks where to board |
| On the plane | 60 s | Leo settles into his seat and repeats the key phrases |

## Important
The embedded mouth movement is a visual placeholder, not phoneme-accurate lip sync. For final dialogue, align mouth-open/closed states to the generated voice waveform or subtitle timing. These are animation-ready vector assets, not rendered final video.
