# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.28

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/capstone/Desktop/project_laser/laser_MJ

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/capstone/Desktop/project_laser/laser_MJ/build

# Include any dependencies generated for this target.
include CMakeFiles/laser_MJ.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/laser_MJ.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/laser_MJ.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/laser_MJ.dir/flags.make

CMakeFiles/laser_MJ.dir/main.cpp.o: CMakeFiles/laser_MJ.dir/flags.make
CMakeFiles/laser_MJ.dir/main.cpp.o: /home/capstone/Desktop/project_laser/laser_MJ/main.cpp
CMakeFiles/laser_MJ.dir/main.cpp.o: CMakeFiles/laser_MJ.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/capstone/Desktop/project_laser/laser_MJ/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/laser_MJ.dir/main.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/laser_MJ.dir/main.cpp.o -MF CMakeFiles/laser_MJ.dir/main.cpp.o.d -o CMakeFiles/laser_MJ.dir/main.cpp.o -c /home/capstone/Desktop/project_laser/laser_MJ/main.cpp

CMakeFiles/laser_MJ.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/laser_MJ.dir/main.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/capstone/Desktop/project_laser/laser_MJ/main.cpp > CMakeFiles/laser_MJ.dir/main.cpp.i

CMakeFiles/laser_MJ.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/laser_MJ.dir/main.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/capstone/Desktop/project_laser/laser_MJ/main.cpp -o CMakeFiles/laser_MJ.dir/main.cpp.s

# Object files for target laser_MJ
laser_MJ_OBJECTS = \
"CMakeFiles/laser_MJ.dir/main.cpp.o"

# External object files for target laser_MJ
laser_MJ_EXTERNAL_OBJECTS =

laser_MJ: CMakeFiles/laser_MJ.dir/main.cpp.o
laser_MJ: CMakeFiles/laser_MJ.dir/build.make
laser_MJ: /usr/local/lib/libopencv_gapi.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_stitching.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_aruco.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_bgsegm.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_bioinspired.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_ccalib.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_dnn_objdetect.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_dpm.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_face.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_freetype.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_fuzzy.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_hdf.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_hfs.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_img_hash.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_line_descriptor.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_reg.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_rgbd.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_saliency.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_sfm.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_stereo.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_structured_light.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_superres.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_surface_matching.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_tracking.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_videostab.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_xfeatures2d.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_xobjdetect.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_xphoto.so.4.0.0
laser_MJ: /usr/local/lib/libJetsonGPIO.so
laser_MJ: /usr/local/lib/libopencv_shape.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_phase_unwrapping.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_optflow.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_ximgproc.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_datasets.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_plot.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_text.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_dnn.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_ml.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_photo.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_video.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_objdetect.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_calib3d.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_features2d.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_flann.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_highgui.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_videoio.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_imgcodecs.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_imgproc.so.4.0.0
laser_MJ: /usr/local/lib/libopencv_core.so.4.0.0
laser_MJ: CMakeFiles/laser_MJ.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/home/capstone/Desktop/project_laser/laser_MJ/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable laser_MJ"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/laser_MJ.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/laser_MJ.dir/build: laser_MJ
.PHONY : CMakeFiles/laser_MJ.dir/build

CMakeFiles/laser_MJ.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/laser_MJ.dir/cmake_clean.cmake
.PHONY : CMakeFiles/laser_MJ.dir/clean

CMakeFiles/laser_MJ.dir/depend:
	cd /home/capstone/Desktop/project_laser/laser_MJ/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/capstone/Desktop/project_laser/laser_MJ /home/capstone/Desktop/project_laser/laser_MJ /home/capstone/Desktop/project_laser/laser_MJ/build /home/capstone/Desktop/project_laser/laser_MJ/build /home/capstone/Desktop/project_laser/laser_MJ/build/CMakeFiles/laser_MJ.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/laser_MJ.dir/depend

