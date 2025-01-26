# Log Uploader for Glenna

Glenna ist ein Discord Bot. Über Glenna organisieren wir unsere wöchentlichen Termine und sie listet unsere vergangenen Logs auf.
Dazu braucht Glenna die Adresse von dps.report und die Anzahl der Versuche die wir brauchten.

Da eine Konfiguration dieses Tools mit der Zeit unübersichtlich und für nicht-Programmierer ohnehin eher unzugänglich gewesen wäre, stelle ich hier auch ein UI zur Verfügung.
Außerdem wollte ich mal mit UI arbeiten und ausprobieren eines zu erstellen.

Kriterien für gezählte Logs:
- Es werden Logs ignoriert, die kleiner als 200 KB sind, um instant gg's rauszufiltern
- Es werden nur Logs an den gewählten Tagen in der gewählten Woche hochgeladen
- Die Logs müssen nach Boss sortiert sein. Unterordner mit Charakteren werden ebenfalls durchsucht, sind aber nicht notwendig.

Nur das neuste Log pro Boss an den gewählten Tagen wird dabei hochgeladen.

Mögliche Auffälligkeiten:
 - Logs, bei denen es zu Fehlern kam, sollten euch am Ende mitgeteilt werden, mit der Option es erneut zu versuchen.
 - Spielt ihr am selben Tag sowohl mit englischem, als auch deutschem Client, werden beide Logs separat behandelt, sofern sich der Encounter Name unterscheidet (bzw. arc Log Ordername).

Wenn ihr Fehler findet oder etwas nicht funktioniert, meldet euch einfach.


Der Upload ist fertig, wenn der Button auf "Done" steht und die Fortschrittsleiste ganz gefüllt ist.
Sollte eins nicht zutreffen, könnt ihr mir das gerne schreiben. Vielleicht können wir den Grund nachvollziehen, um diesen Fehler in Zukunft zu beheben.

Die Ausgabe sieht dann folgendermaßen aus:

```
https://dps.report/1111-20200216-214025_ice 1
https://dps.report/1111-20200216-210840_cairn 1
https://dps.report/1111-20200216-213209_dei 1
https://dps.report/1111-20200216-205300_kc 1
https://dps.report/1111-20200216-202720_trio 2  .... yes
https://dps.report/1111-20200216-203516_matt 1
https://dps.report/1111-20200216-195527_gors 1
https://dps.report/1111-20200216-205510_tc 1
https://dps.report/1111-20200216-200308_sab 1
https://dps.report/1111-20200216-201033_sloth 1
https://dps.report/1111-20200216-212050_sam 1
https://dps.report/1111-20200216-194308_vg 1
https://dps.report/1111-20200216-211307_mo 1
https://dps.report/1111-20200216-210234_xera 1
https://dps.report/1111-20200216-214748_falln 1
```

Dies ist jeweils ein Link zu dps.report, sowie die Anzahl der Versuche, die an diesen Tagen der Woche dort benötigt wurden.

# Build
Um die ausführbare Datei zu erhalten, braucht es pyinstaller mit folgendem Kommando aus dem venv des Projects:
`python -m PyInstaller -F -w -n "Log Uploader for Glenna v3.1" -i "glenna_uploader.ico" --add-data "src\uploader\const\config.yaml;." "src\uploader\app.py"
`

- `-F --onefile` create a one-file bundled executable
- `-w --windowed` removes the console window that would otherwise appear
- `-n --name` defines the name of the application
- `-i --icon` set an .ico as executable icon (on windows)
- `--add-data` was used to add the icon file to the executable. It was then extracted into a temp folder on launch
  - the path is under sys _MEIPASS

# Known Issues

> AttributeError: 'CTkToolTip' object has no attribute 'block_update_dimensions_event'

This error seems to be triggered if a tooltip is shown on a different monitor, with either a different resolution
or a different Windows Scaling setting, than the original monitor of the window.
The tooltip might break, i.e. not have a background. And the scaling will not work if moving back to the other monitor.

Not sure if there's a workaround. Hoping for a upstream fix. Might consider different Tooltip libraries for Tkinter.

