# GMod Data Folder Backup Tool (GMDFBT)

A one-click backup and restore tool for your Garry's Mod `data` folder. Powered by PyQt5.

---

## Usage

### Basic

1. Run `GMDFBT` (as Administrator if prompted — see FAQ).
2. The source folder defaults to `C:\Program Files (x86)\Steam\steamapps\common\GarrysMod\garrysmod\data`.
3. The destination folder defaults to `Documents\GMod Data Folder Backups`.
4. Press **Create Backup**.
5. A success dialog will appear when done. Close the app.

> The app may briefly freeze during the backup process — this is normal.

---

### Advanced

#### Restoring a Backup
1. Open the **Mode** dropdown and select **Restore**.
2. Set the **Backup Source** to the backup folder you want to restore from.
3. The **Restore Target** defaults to your GMod `data` folder.
4. Press **Restore Backup** and confirm the warning dialog.

> **Warning:** Restoring will permanently delete everything in the restore target and replace it with the backup. This cannot be undone. This feature is in early beta — manual restoration via the file manager is safer.

#### Additional Settings
Click **Additional Settings** to open the settings dialog. Available options:

| Setting | Description |
|---|---|
| Backup folder name format | Customize the backup folder name. Supports `{date}` and `{time}` placeholders. Default: `backup-{date}-{time}` |
| Enforce 1 GB folder size limit | Prevents backups larger than 1 GB. Disable to allow larger folders. |
| Enable logging folder | Writes a `.log` file to a `logs/` folder next to the app after each backup. |
| Compress backup into .zip file | Compresses the finished backup folder into a `.zip` archive. |
| Theme | Switch between **Dark** and **Light** themes. |

Settings are saved to `settings.json` next to the app. Some settings require a restart to take effect.

#### Live Log
Check **Show live log** before starting a backup or restore to see a real-time list of every file and folder being processed.

#### Command-Line Mode (Headless)
You can run the app without the GUI by passing the source and destination as arguments:

```
GMDFBT.exe "C:\path\to\data" "C:\path\to\destination"
```

This runs an immediate backup using the default format (`backup-{date}-{time}`) with the 1 GB size restriction enabled and no logging.

#### Update Checks
On startup, the app automatically checks GitHub for a newer version and shows a notification if one is available.

---

## FAQ

### Basic functionality

**Q: Do I have to run it as Administrator?**
You don't have to, but it's strongly recommended. Without admin privileges, some files may fail to copy. If you run without admin rights, the app will warn you and offer a "Run Anyway" option.

**Q: Can I back up a folder other than the GMod data folder?**
Yes. Use the **Browse** button next to the source field to select any folder, or type the path directly.

**Q: Can I change where backups are saved?**
Yes. Use the **Browse** button next to the destination field, or type the path directly.

**Q: What does the backup folder name format do?**
It controls the name of the folder created inside your destination. For example, `backup-{date}-{time}` produces a folder like `backup-03-30-2026-14-22-05`. You can use any combination of text, `{date}`, and `{time}`.

**Q: Does compressing a backup delete the original backup folder?**
No. The app creates a `.zip` file alongside the backup folder. The uncompressed folder is kept.

**Q: Where are log files saved?**
When logging is enabled, `.log` files are saved to a `logs/` folder created next to the app executable.

**Q: Can I restore from a `.zip` backup?**
The restore feature currently expects a folder. Restoring directly from a `.zip` file is not supported — extract the `.zip` first, then restore from the extracted folder.

---

### Error related

**Q: The app shows "Corrupted Settings" on startup.**
The `settings.json` file is malformed or unreadable. Delete `settings.json` from the app's folder and restart. The app will recreate it with default values.

**Q: Backup failed with "Folder exceeds size restriction of 1 GB".**
Your GMod `data` folder is larger than 1 GB. Go to **Additional Settings** and uncheck **Enforce 1 GB folder size limit**, then try again.

**Q: Backup failed with "Source folder does not exist".**
The path in the source field does not exist on your system. Verify your GMod installation path and update the source field accordingly.

**Q: The restore failed with a PermissionError about a protected directory.**
GMDFBT blocks restores into system-critical directories (e.g. `C:\Windows`, `C:\Program Files`, `C:\Users`) to prevent accidental data loss. Choose a valid restore target such as your GMod `data` folder.

**Q: What do the error codes mean?**
Error dialogs include a numeric code to help identify the type of error:

| Code | Type |
|---|---|
| 1001 | ValueError |
| 1002 | TypeError |
| 1006 | FileNotFoundError |
| 1007 | IOError |
| 1011 | OSError |
| 1012 | RuntimeError |
| 1018 | JSONDecodeError |

If an error is non-critical, the app will offer to continue running. If critical, it will close.

---

## Changelog

### 1.1.0-beta.2 (current)
- Added **Restore** mode with protection against writing to critical system directories
- Added startup **update check** against GitHub tags
- Added **compress backup** option (`.zip`)
- Added **Dark / Light theme** toggle
- Added **command-line (headless) mode**
- Added live log visibility toggle
- Added `settings.json` persistence for all settings
- Improved error dialogs with error type names and numeric codes
- Progress bar shown during both backup and restore

### 1.0.x
- Initial release
- One-click backup of the GMod `data` folder
- Configurable source and destination paths
- Custom backup folder name format with `{date}` / `{time}` tokens
- Optional 1 GB size restriction
- Optional file logging

---

## Support

For questions or bug reports, DM **thethirdpuddle** on Discord.

To report issues, open a ticket at: https://github.com/TheThirdPuddle/GMod-Data-Folder-Backup-Tool/issues

---

## Credits

| Contributor | Role |
|---|---|
| **Thethirdpuddle** | Original concept, design, and documentation |
| **ChatGPT** | Assistance with code and disclaimer writing |

---

## License

GMDFBT is free software licensed under the **GNU General Public License v3.0**.

You are free to use, modify, and distribute this software under the terms of the GPL v3. See the [LICENSE](LICENSE) file for the full license text, or visit https://www.gnu.org/licenses/gpl-3.0.html.

**Disclaimer:** This software is provided "as is", without any warranties of any kind. The authors accept no liability for data loss, damage, or corruption resulting from use of this software. By using GMDFBT, you accept full responsibility for any outcomes and acknowledge the potential risks involved.
