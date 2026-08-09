cmake_minimum_required(VERSION 3.12)

project(SkyGeo VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

file(
    GLOB experiment_dirs
    LIST_DIRECTORIES true
    "${PROJECT_SOURCE_DIR}/experiments/*"
)

foreach(dir ${experiment_dirs})

    if(IS_DIRECTORY ${dir})

        get_filename_component(target_name ${dir} NAME)

        file(
            GLOB sources
            CONFIGURE_DEPENDS
            "${dir}/*.cpp"
        )

        if(sources)

            add_executable(
                ${target_name}
                ${sources}
            )

            target_include_directories(
                ${target_name}
                PRIVATE
                ${PROJECT_SOURCE_DIR}/include
            )

            # 告诉当前 experiment：
            # visualize.out 应该生成在哪里
            target_compile_definitions(
                ${target_name}
                PRIVATE
                SKYGEO_VIS_FILE="${dir}/visualize.out"
            )

            message(
                STATUS
                "Added experiment: ${target_name}"
            )

        endif()

    endif()

endforeach()