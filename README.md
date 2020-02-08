# Log Uploader for Glenna

Aus der Idee, ein Skript zu schreiben, dass für meine Raid Gruppe die wöchentlichen Logs hochläd enstanden.

Da die Konfiguration im Code recht nervig geworden wäre - und ich es mal ausprobieren wollte - hab ich ein UI drum herum gebaut.

Es werden logs ausgewählt, die:
 - in einem der Boss Ordner oder eins darunter (bei Sortierung nach Charakteren) liegen
 - größer sind als 200KB
 - in der Woche bzw. an dem Tag erstellt wurden, die eingestellt sind, wenn der Button gedrück wird

Nur der neuste Log wird dabei hochgeladen.

Es kann zu Fehlern kommen:
 - sollte der Upload zu oft nicht funktionieren, wird das Log ausgelassen
 - bei nochmaligem drücken des Start Buttons während dieser läd (und nicht hängt) => bringt die Ausgabe durcheinander
 - solltet ihr am selben Tag mit deutscher und englischer Sprache Boss mehrfach legen, werden diese seperat hochgeladen..
 - was ich vergessen/noch nicht gesehen habe

Von den Fehlern solltet ihr allerdings nichts sehen. Das Programm würde einfach nichts tun.

Wenn der Upload fertig ist ("Done" und Balken voll gefüllt), könnt ihr die Logs mit "Copy to Clipboard" kopieren.

Die Ausgabe sieht dann folgendermaßen aus:

```
https://dps.report/Kf6U-20200205-192401_sh Seelenloser Schrecken 1
https://dps.report/63Hp-20200205-192925_rr Fluss der Seelen 1
https://dps.report/Pmrb-20200205-193835_bk Bezwungener König 1
https://dps.report/BEFr-20200205-194236_se Seelenverzehrer 1
https://dps.report/8UDr-20200205-194542_eyes Augen 1
https://dps.report/m6GV-20200205-200534_dhuum Dhuum 3
https://dps.report/XSwc-20200205-201418_ca Beschworene Verschmelzung 1
https://dps.report/L6k4-20200205-202446_twins Largos-Zwillinge 1
https://dps.report/d5pX-20200205-204126_qadim Qadim 1
https://dps.report/j59y-20200205-210908_adina Kardinal Adina 1
https://dps.report/fgb5-20200205-205902_sabir Kardinal Sabir 1
https://dps.report/pGqE-20200205-212050_qpeer Qadim der Unvergleichliche 1
```

Dies entspricht dem Permalink zum hochgeladenen dps.report File, dem Bossnamen (Name des Ordners => englischer Client = englische Bossnamen) und der Anzahl der Versuche.
