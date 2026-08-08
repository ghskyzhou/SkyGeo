cmake_minimum_required(VERSION 3.12)

project(SkyGeo VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 找到 experiments 下的所有一级子目录
file(
    GLOB experiment_dirs
    LIST_DIRECTORIES true
    "${PROJECT_SOURCE_DIR}/experiments/*"
)

foreach(dir ${experiment_dirs})

    # 只处理文件夹
    if(IS_DIRECTORY ${dir})

        # 取文件夹名字，例如：
        # experiments/test -> test
        get_filename_component(target_name ${dir} NAME)

        # 找这个文件夹里的所有 cpp
        file(
            GLOB sources
            CONFIGURE_DEPENDS
            "${dir}/*.cpp"
        )

        # 如果里面确实存在 cpp 才创建程序
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

            message(
                STATUS
                "Added experiment: ${target_name}"
            )

        endif()

    endif()

endforeach()