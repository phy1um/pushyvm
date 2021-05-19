
DOCFILES=spec.html
STYLE=milligram.min.css

docs: $(DOCFILES)

%.html: %.md
	pandoc -s -c $(STYLE) $< -o $@


