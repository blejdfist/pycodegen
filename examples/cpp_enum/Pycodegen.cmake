set(PYCODEGEN_BIN "pycodegen")

function(CODEGEN)
    cmake_parse_arguments(CODEGEN "" "FRONTEND;DRIVER;OUTPUT_VAR" "INPUT_FILES" ${ARGN})

    message(STATUS "Configuring code generation")
    message(STATUS "  Frontend: ${CODEGEN_FRONTEND}")
    message(STATUS "  Input: ${CODEGEN_INPUT_FILES}")
    message(STATUS "  Driver: ${CODEGEN_DRIVER}")

    foreach(INPUT ${CODEGEN_INPUT_FILES})
        execute_process(
            COMMAND ${PYCODEGEN_BIN} ${CODEGEN_FRONTEND}
            ${CMAKE_CURRENT_SOURCE_DIR}/${INPUT}
            --driver ${CMAKE_CURRENT_SOURCE_DIR}/${CODEGEN_DRIVER}
            --list-deps
            RESULT_VARIABLE retcode
            OUTPUT_VARIABLE dependencies
            OUTPUT_STRIP_TRAILING_WHITESPACE
        )

        if(NOT retcode EQUAL 0)
            message(FATAL_ERROR "codegen: Unable to get dependencies")
        else()
            message(STATUS "  Inputs: ${dependencies}")
        endif()

        execute_process(
            COMMAND ${PYCODEGEN_BIN} ${CODEGEN_FRONTEND}
            ${CMAKE_CURRENT_SOURCE_DIR}/${INPUT}
            --driver ${CMAKE_CURRENT_SOURCE_DIR}/${CODEGEN_DRIVER}
            --output-dir ${CMAKE_BINARY_DIR}/generated
            --list-output
            RESULT_VARIABLE retcode
            OUTPUT_VARIABLE outputs
            OUTPUT_STRIP_TRAILING_WHITESPACE
        )

        if(NOT retcode EQUAL 0)
            message(FATAL_ERROR "codegen: Unable to list of outputs")
        else()
            message(STATUS "  Output: ${outputs}")
            set(${CODEGEN_OUTPUT_VAR} "${outputs}" PARENT_SCOPE)
        endif()

        add_custom_command(
            OUTPUT ${outputs}
            COMMAND ${PYCODEGEN_BIN}
            ARGS cpp ${CMAKE_CURRENT_SOURCE_DIR}/${INPUT}
                 --driver ${CMAKE_CURRENT_SOURCE_DIR}/${CODEGEN_DRIVER}
                 --output-dir ${CMAKE_BINARY_DIR}/generated
            DEPENDS
                ${CMAKE_CURRENT_SOURCE_DIR}/${INPUT}
                ${CMAKE_CURRENT_SOURCE_DIR}/${CODEGEN_DRIVER}
                ${dependencies}
        )
  endforeach()
endfunction()

