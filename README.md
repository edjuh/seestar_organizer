# Terpen Tijn Observatory Pipeline
## Hardware Environment
- **Controller:** RPi5 (User: ed)
- **Primary Storage:** /mnt/astronas (CIFS)
- **Telescope Source:** /mnt/seestar (SMB)
- **Local Buffer:** /home/ed/seestar_organizer/data/local_buffer

## Active Services
- `harvester.service`: Moves FITS from Telescope to NAS.
- `analyst.service`: Performs photometry and AAVSO reporting.

## Troubleshooting
- `journalctl -u harvester.service -f`
- `journalctl -u analyst.service -f`
