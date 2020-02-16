# Log Uploader for Glenna

Aus der Idee, ein Skript zu schreiben, dass für meine Raid Gruppe die wöchentlichen Logs hochläd enstanden.

Da die Konfiguration im Code recht nervig geworden wäre - und ich es mal ausprobieren wollte - hab ich ein UI drum herum gebaut.

Auswahl der Logs:
- Es werden Logs ignoriert, die kleiner als 200KB sind
- Es werden nur Logs an den gewählten Tagen in der gewählten Woche hochgeladen
- Die Logs müssen nach Boss sortiert sein. Unterordner mit Charakteren werden ebenfalls durchsucht, sind aber nicht notwendig.

Nur der neuste Log pro Boss an den gewählten Tagen wird dabei hochgeladen.

Mögliche Auffälligkeiten:
 - Logs, bei denen es zu Fehlern kam, sollten euch am Ende mitgeteilt werden, mit der Option es erneut zu versuchen.
 - Spielt ihr am selben Tag sowohl mit englischem, als auch deutschem Client, werden beide seperat behandelt.

Wenn ihr Fehler findet oder etwas nicht funktioniert, meldet euch einfach.


Der Upload ist fertig, wenn der Button auf "Done" steht und die Fortschrittsleiste ganz gefüllt ist.
Sollt eins nicht zutreffen, könnt ihr mir das gerne schreiben. Vielleicht können wir den Grund nachvollziehen.

Die Ausgabe sieht dann folgendermaßen aus:

```
https://dps.report/1111-20200216-214025_ice 1
https://dps.report/1111-20200216-210840_cairn 1
https://dps.report/1111-20200216-213209_dei 1
https://dps.report/1111-20200216-205300_kc 1
https://dps.report/1111-20200216-202720_trio 2
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