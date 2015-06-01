BASE_DIR=griffin

.PHONY: install
.PHONY: uninstall
install:
	pip install -U .
	
uninstall:
	pip uninstall .

.PHONY: test
test:
	./runtests.sh $(BASE_DIR)

.PHONY: clean
clean:
	for f in $(shell find -iname '*.pyc'); do \
		rm -fr $$f; \
	done;