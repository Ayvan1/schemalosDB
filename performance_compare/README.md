Bei den Tests zeigte sich, dass InfluxDB schneller beim Einfügen von Zeitreihendaten ist, während Oracle die Lese- und Löschoperationen schneller durchführt.

Begründung:
InfluxDB ist speziell für hohe Schreibraten optimiert und nutzt eine append-only Speicherstruktur, die schnelle Inserts ermöglicht. Oracle hingegen ist ein relationales Datenbanksystem mit effizienten Indexierungen und optimierten Abfrageplänen, was Lese- und Löschvorgänge beschleunigt, jedoch die Schreibgeschwindigkeit durch zusätzliche Verwaltungsaufwände etwas bremst.