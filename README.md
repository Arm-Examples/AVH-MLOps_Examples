# AVH-MLOps_Examples
This repo contains various example projects that show how to use the CMSIS-Toolbox workflows in an MLOps context.

## Directory Structure

Directory           | Description
:-------------------|:------------------------------
[.github/workflows](./.github/workflows)           | GitHub Action workflow definitions.
[AVH-MLOps-main](./AVH-MLOps-main)                 | Simple "Hello World" test project with vcpkg installation for desktop usage.
[mlek-kws](./mlek-kws)                             | MLEK Keyword Spotting (KWS) example with generation of a ML Model library and execution on AVH. This project runs on all relevant Cortex-M and Ethos-U targets and can be compiled using different toolchains.
[QeexoAutoML](./QeexoAutoML)                       | Qeexo AutoML example with prebuilt ML library and test execution.
[TFLmicrospeech](./TFLmicrospeech)                 | TensorFLow Lite Microspeech example with ML library generation and test execution. This project runs on all relevant Cortex-M and Ethos-U targets and can be compiled using different toolchains.

Github Action workflow templates

Every example on this repository has a Github Actions based CI flow that will build the project and run it on a Arm Virtual Hardware model. These workflows are: 

- **.github/workflows/build_MLEK_kws.yml**
- **.github/workflows/build_QeexoML.yml**
- **.github/workflows/build_TFLmicrospeech.yml**


## Known Issues

The following items are at this moment not completed:

- Consistent support for GCC and LLVM compiler. Currently only Arm Compiler 6 is supported.
- Multiple demo projects for VSI usage (Sensor, Audio, Video) will be added.
- Arm Virtual Models are not yet available for vcpkg installation; use classic MDK version 5 for using AVH models.
