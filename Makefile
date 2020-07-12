test:
	@which python3
	@python3 -c "import tatsu"
	@python3 -c "import llvmlite"
	@file ./compiladoresAAE