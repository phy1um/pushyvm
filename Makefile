
DOCFILES=docs/spec.html
STYLE=milligram.min.css
COMPILE=compile.py

docs: $(DOCFILES)

%.html: %.md
	pandoc -s -c $(STYLE) $< -o $@

%.bin: %.svm
	python3 $(COMPILE) $< $@
