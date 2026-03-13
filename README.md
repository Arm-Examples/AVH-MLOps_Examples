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
[scripts](./scripts)                               | Scripts for searching and summarizing vcpkg configuration files across GitHub organizations.

## GitHub Action Workflows

### Example Build & Run Workflows

Every example on this repository has a GitHub Actions based CI flow that will build the project and run it on an Arm Virtual Hardware model. These workflows are:

- **.github/workflows/build_MLEK_kws.yml**
- **.github/workflows/build_QeexoML.yml**
- **.github/workflows/build_TFLmicrospeech.yml**

### vcpkg Configuration Search Workflow

The workflow [**.github/workflows/search_vcpkg_configurations.yml**](./.github/workflows/search_vcpkg_configurations.yml) (together with the helper script [**scripts/search_vcpkg_configs.py**](./scripts/search_vcpkg_configs.py)) scans the following GitHub organizations for `vcpkg-configuration.json` and `vcpkg-run-configuration.json` files and summarises the findings in **[vcpkg_configurations.csv](./vcpkg_configurations.csv)**:

- [Arm-Examples](https://github.com/Arm-Examples/)
- [Arm-Software](https://github.com/Arm-Software/)
- [Open-CMSIS-Pack](https://github.com/Open-CMSIS-Pack/)
- [MDK-packs](https://github.com/MDK-packs/)

The CSV contains one row per repository with the following columns:

| Column | Description |
|--------|-------------|
| `repository_url` | Link to the GitHub repository |
| `vcpkg-configuration.json` | Full content of the `vcpkg-configuration.json` file(s) found |
| `vcpkg-run-configuration.json` | Full content of the `vcpkg-run-configuration.json` file(s) found |

The workflow runs automatically every Monday at 06:00 UTC and can also be triggered manually via **Actions → Search vcpkg Configuration Files → Run workflow**. The resulting CSV is uploaded as a workflow artifact and, when running on the default branch, committed back to the repository.

The script can also be run locally:

```bash
python3 scripts/search_vcpkg_configs.py --token <your-github-token> --output vcpkg_configurations.csv
```


## Known Issues

The following items are at this moment not completed:

- Consistent support for GCC and LLVM compiler. Currently only Arm Compiler 6 is supported.
- Multiple demo projects for VSI usage (Sensor, Audio, Video) will be added.
- Arm Virtual Models are not yet available for vcpkg installation; use classic MDK version 5 for using AVH models.
