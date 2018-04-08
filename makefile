CXXFLAGS    += `pkg-config opencv --cflags`

LDFLAGS     += `pkg-config opencv --libs`

compile:
	cythonize pydarknet.pyx --annotate -s LANGUAGE="c++"
	g++ -I"/usr/local/lib/python3.5/dist-packages/numpy/core/include" -I"$DARKNET_HOME/include" -I"$DARKNET_HOME/src" -I"/usr/include/python3.5" $(CXXFLAGS) -c pydarknet.c -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -std=c++14
	g++ -I"$DARKNET_HOME/include" -I"$DARKNET_HOME/src" -I"/usr/include/python3.5" $(CXXFLAGS) -c bridge.cpp -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -std=c++14


link:
	g++ -o pydarknet.so pydarknet.o bridge.o $(LDFLAGS) "$DARKNET_HOME/libdarknet.so" -L"/usr/lib/python3.5/config-3.5m-x86_64-linux-gnu" -lpython3.5 -lpthread -shared -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing

all: compile link

clean:
	rm pydarknet.o
	rm bridge.o
	rm pydarknet.c
	rm pydarknet.so
	rm pydarknet.html