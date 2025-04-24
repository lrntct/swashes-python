# Minimum CMake version required (FetchContent needs >= 3.11, using 3.18 as per pyproject)
cmake_minimum_required(VERSION 3.18)

# Set recommended policies
cmake_policy(SET CMP0135 NEW) # Use extraction time for FetchContent timestamps

# Define the project name (can be different from the Python package name)
project(swashes_build LANGUAGES CXX C) # Assuming C/C++ needed by upstream

# Include the FetchContent module for downloading external dependencies
include(FetchContent)

# --- Fetch Upstream SWASHES Source ---
message(STATUS "Declaring FetchContent for SWASHES")
FetchContent_Declare(
    swashes_upstream # Name for this dependency in CMake
    URL https://sourcesup.renater.fr/frs/download.php/file/6718/SWASHES-1.05.00.zip
    # Optional: Add URL_HASH SHA256=... for checksum verification if known
)

# Make the content available (downloads and extracts if not already done)
# This populates swashes_upstream_SOURCE_DIR and swashes_upstream_BINARY_DIR
# By default, source is extracted to: ${CMAKE_BINARY_DIR}/_deps/swashes_upstream-src
# We specify SOURCE_DIR to potentially place it elsewhere if needed, but default is fine.
message(STATUS "Making FetchContent available for SWASHES")
FetchContent_MakeAvailable(swashes_upstream)

# Check if the source directory variable is populated (should be)
if(NOT swashes_upstream_SOURCE_DIR)
    message(FATAL_ERROR "swashes_upstream_SOURCE_DIR is not defined after FetchContent_MakeAvailable")
endif()
message(STATUS "SWASHES source directory: ${swashes_upstream_SOURCE_DIR}")

# --- Build Upstream SWASHES using Makefile ---
message(STATUS "Adding custom command to build SWASHES using make")

# Define the path to the expected executable after make runs
# The upstream Makefile seems to place it in a 'bin' subdirectory
set(SWASHES_EXECUTABLE ${swashes_upstream_SOURCE_DIR}/bin/swashes)

# Add a custom command that runs 'make' in the source directory.
# This command is attached to a custom target to ensure it runs during the build.
# The OUTPUT specifies the file this command is expected to produce.
add_custom_command(
    OUTPUT ${SWASHES_EXECUTABLE} # Updated path
    # Explicitly use 'make'. Let make find/use its own compilers.
    COMMAND make
    WORKING_DIRECTORY ${swashes_upstream_SOURCE_DIR}
    COMMENT "Building SWASHES executable with make..."
    VERBATIM # Ensure commands are not escaped
    DEPENDS ${swashes_upstream_SOURCE_DIR}/Makefile # Re-run if Makefile changes (optional but good practice)
)

# Add a custom target that depends on the output of the custom command.
# Building this target triggers the custom command.
add_custom_target(
    build_swashes_upstream ALL # Add ALL to build this target by default
    DEPENDS ${SWASHES_EXECUTABLE}
    COMMENT "Ensuring SWASHES upstream is built"
)

# --- Install the Built Executable ---
message(STATUS "Installing SWASHES executable to bin directory")

# Install the compiled 'swashes' executable into a 'bin' directory
# relative to the package installation prefix.
install(
    PROGRAMS ${SWASHES_EXECUTABLE}
    DESTINATION bin  # Installs to <prefix>/bin
    COMPONENT swashes_runtime # Optional component name
)

# The dependency is handled by the DEPENDS keyword in add_custom_target.
# The install command implicitly depends on the file existing.
# No explicit add_dependencies needed here.

message(STATUS "CMake configuration for SWASHES wrapper finished.")