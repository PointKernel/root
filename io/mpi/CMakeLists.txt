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

ROOT_GENERATE_DICTIONARY(G__RMPI ${headers} STAGE1 MODULE RMPI LINKDEF LinkDef.h DEPENDENCIES Physics RIO)

ROOT_OBJECT_LIBRARY(RMPIObjs G__RMPI.cxx ${sources})

ROOT_LINKER_LIBRARY(RMPI $<TARGET_OBJECTS:RMPIObjs> $<TARGET_OBJECTS:RootPcmObjs>
                               LIBRARIES ${CMAKE_DL_LIBS} MPI::MPI_CXX
                               DEPENDENCIES Physics RIO)

ROOT_INSTALL_HEADERS()

ROOT_ADD_TEST_SUBDIRECTORY(test)
