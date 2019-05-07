############################################################################
# CMakeLists.txt file for building ROOT io/mpi package
############################################################################

set(headers JetEvent.h
   TClientInfo.h
   TMPIFile.h
)

set(sources src/JetEvent.cxx
   src/TClientInfo.cxx
   src/TMPIFile.cxx
)

include_directories(${MPI_CXX_HEADER_DIR})

ROOT_GENERATE_DICTIONARY(G__RMPI ${headers} STAGE1 MODULE RMPI LINKDEF LinkDef.h DEPENDENCIES Core Thread)

ROOT_OBJECT_LIBRARY(RMPIObjs G__RMPI.cxx ${sources})

ROOT_LINKER_LIBRARY(RMPI $<TARGET_OBJECTS:RMPIObjs> $<TARGET_OBJECTS:RootPcmObjs>
                               LIBRARIES ${CMAKE_DL_LIBS}
                               DEPENDENCIES Core Thread)

ROOT_INSTALL_HEADERS()

ROOT_ADD_TEST_SUBDIRECTORY(test)
