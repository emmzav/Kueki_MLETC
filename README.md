# Kueski_mletc user dataproc

This application consist of 3 modules: 
1) **create_features**.- It generates the features to be used to train the model and predict results. 
2) **model_train**.-  It trains the model using the generated features.
3) **model_predict**.-  It generates the prediction of the risk of a client according yo

##  Module 1: ABT

This module builds an abt parquet for the input of the kmeans module: A table that contain all the necessary variables in all the process. 
An example of command line used for launching this module is a follows:

```
sparkutils-submit worker.py tests_resources/config_files/01_ABT/params_local_abt.conf
```

The local_abt.conf file contents should have the following structure:

```
{
    lkcol_attrition_tdc{
        stage_name = process_01_ABT
        class_name = ControllerABTProcess
        actual_date = ${?DATE}
        input{
            tla117{
                path = tests_resources/inputs/t_mdco_tla117_cte_fide_bo_pyt/
                partition_field = cutoff_date
                end_date = cutoff_date
                months_back = 11
                is_monthly = 1
                class_namings = CustomerLoyalty
            }
            tla610{
                path = tests_resources/inputs/t_mdco_tla610_cap_cto_pyt/
                partition_field = cutoff_date
                end_date = cutoff_date
                months_back = 11
                is_monthly = 1
                class_namings = ContractCatchmentPyt
            }
            tla813{
                path = tests_resources/inputs/t_mdco_tla813_tdc_promo_pyt/
                partition_field = cutoff_date
                end_date = cutoff_date
                months_back = 11
                is_monthly = 1
                class_namings = TdcPromotionsPyt
            }
            tla102{
                path = tests_resources/inputs/t_mdco_tlc102_buro_c_credito/
                partition_field = cutoff_date
                end_date = cutoff_date
                months_back = 11
                is_monthly = 1
                class_namings = CreditBureau
            }
        }
        output{
            path_abt = tests_resources/output/abt/
        }
        schemas{
            abt_schema =  tests_resources/schemas/attrtdcunifyabt.output.schema
        }
    }
}
```

Where DATE must be defined as an environment variable with format yyyy-mm-dd 


##  Module 2: Kmeans

This module builds 6 parquets: 
A table for each cluster: MSI, EFI, High_Use, Premium, Seminew and Neutral. Each table contain the necessary columns to be use in the train and score of an Gradiente Boosting Classifier Tree model.
```
sparkutils-submit worker.py tests_resources/config_files/02_Kmeans/params_local_kmeans_score.conf
```

The params_local_kmeans_score.conf file contents should have the following structure:

```
{
    lkcol_attrition_tdc{
        stage_name = process_02_Kmeans
        class_name = ControllerScoreProcess
        actual_date = ${?DATE}

        input{
            model_path = tests_resources/inputs/kmeans/
            path_abt = tests_resources/output/abt/
        }
        output{
            path_cluster_premium_df = tests_resources/output/cluster_premium_df
            path_cluster_high_use_df =  tests_resources/output/cluster_high_use_df
            path_cluster_efi_df = tests_resources/output/cluster_efi_df
            path_cluster_msi_df = tests_resources/output/cluster_msi_df
            path_cluster_neutral_df = tests_resources/output/cluster_neutral_df
            path_seminew_df = tests_resources/output/seminew_df
        }
        schemas{
            premium_schema =  tests_resources/schemas/attrtdcpremiumabt.output.schema
            efi_schema = tests_resources/schemas/attrtdcefiabt.output.schema
            seminew_schema = tests_resources/schemas/attrtdcseminewabt.output.schema
            high_use_schema = tests_resources/schemas/attrtdchighuseabt.output.schema
            msi_schema = tests_resources/schemas/attrtdcmsiabt.output.schema
            neutral_schema = tests_resources/schemas/attrtdcneutralabt.output.schema
        }
    }
}

```
Where DATE must be defined as an environment variable with format yyyy-mm-dd 


##  Module 3: Target Creation

This module builds one parquets: This table contain a flag that indicate if a customer has cancelled in the last months. This table is going to be used for the train of the Gradient Boosting Tree classifier models. 
```
sparkutils-submit worker.py tests_resources/config_files/03_TargetCreation/params_local_target.conf
```

The params_local_target.conf file contents should have the following structure:

```
{
    lkcol_attrition_tdc{
        stage_name = process_03_TargetCreation
        class_name = ControllerTargetCreation
        date = ${?DATE}
        input{
            tla813{
                path = tests_resources/inputs/t_mdco_tla813_tdc_promo_pyt/
                partition_field = cutoff_date
                end_date = cutoff_date
                months_back = 5
                is_monthly = 1
                class_namings = TdcPromotionsPyt
            }
        }
        output{
            path_target = tests_resources/output/target/
        }
        schemas{
            target_schema = tests_resources/schemas/attrtdctarget.output.schema
        }
    }
}
```
Where DATE must be defined as an environment variable with format yyyy-mm-dd 


##  Module 4: GBoost

This module builds one temporary table and for each config file one Gradient Boosting Classifier model.
The temporary table has contain only one value for each cluster.
This module is going to be execute 6 times, one for each config file, that containt the info of one corresponding cluster, so the module generates 6 GBoost models.
```
sparkutils-submit worker.py tests_resources/config_files/04_GBoost/params_local_gboost_train_efi.conf
sparkutils-submit worker.py tests_resources/config_files/04_GBoost/params_local_gboost_train_msi.conf
sparkutils-submit worker.py tests_resources/config_files/04_GBoost/params_local_gboost_train_neutro.conf
sparkutils-submit worker.py tests_resources/config_files/04_GBoost/params_local_gboost_train_premium.conf
sparkutils-submit worker.py tests_resources/config_files/04_GBoost/params_local_gboost_train_high_use.conf
sparkutils-submit worker.py tests_resources/config_files/04_GBoost/params_local_gboost_train_seminew.conf
```

The params_local_gboost_train_efi.conf file contents should have the following structure:

```
{
    lkcol_attrition_tdc{
        stage_name = process_04_GBoost
        class_name = ControllerTrainGboost
        actual_date = "2018-12-01"
        cluster = "EFI"

        input{
            path_cluster = tests_resources/output/cluster_efi_df/
            path_target = tests_resources/output/target/
        }
        output{
            path_gboost = tests_resources/output/gboost_efi/
            path_ks = tests_resources/output/ks/
        }
    }
}
```

The params_local_gboost_train_msi.conf file contents should have the following structure:

```
{
    lkcol_attrition_tdc{
        stage_name = process_04_GBoost
        class_name = ControllerTrainGboost
        actual_date = "2018-12-01"
        cluster = "MSI"
        input{
            path_cluster = tests_resources/output/cluster_msi_df/
            path_target = tests_resources/output/target/
        }
        output{
            path_gboost = tests_resources/output/gboost_msi/
            path_ks = tests_resources/output/ks/
        }
    }
}
```

The params_local_gboost_train_neutro.conf file contents should have the following structure:

```
{
    lkcol_attrition_tdc{
        stage_name = process_04_GBoost
        class_name = ControllerTrainGboost
        actual_date = "2018-12-01"
        cluster = "NEUTRO"
        input{
            path_cluster = tests_resources/output/cluster_neutral_df/
            path_target = tests_resources/output/target/
        }
        output{
            path_gboost = tests_resources/output/gboost_neutral/
            path_ks = tests_resources/output/ks/
        }
    }
}
```

The params_local_gboost_train_high_use.conf file contents should have the following structure:

```
{
    lkcol_attrition_tdc{
        stage_name = process_04_GBoost
        class_name = ControllerTrainGboost
        actual_date = "2018-12-01"
        cluster = "ALTA_UTILIZACION"
        input{
            path_cluster = tests_resources/output/cluster_high_use_df/
            path_target = tests_resources/output/target/
        }
        output{
            path_gboost = tests_resources/output/gboost_high_use/
            path_ks = tests_resources/output/ks/
        }
    }
}
```

The params_local_gboost_train_premium.conf file contents should have the following structure:

```
{
    lkcol_attrition_tdc{
        stage_name = process_04_GBoost
        class_name = ControllerTrainGboost
        actual_date = "2018-12-01"
        cluster = "PREMIUM"
        input{
            path_cluster = tests_resources/output/cluster_premium_df/
            path_target = tests_resources/output/target/
        }
        output{
            path_gboost = tests_resources/output/gboost_premium/
            path_ks = tests_resources/output/ks/
        }
    }
}
```

The params_local_gboost_train_seminew.conf file contents should have the following structure:

```
{
    lkcol_attrition_tdc{
        stage_name = process_04_GBoost
        class_name = ControllerTrainGboost
        actual_date = "2018-12-01"
        cluster = "SEMINUEVO"
        input{
            path_cluster = tests_resources/output/seminew_df/
            path_target = tests_resources/output/target/
        }
        output{
            path_gboost = tests_resources/output/gboost_seminew/
            path_ks = tests_resources/output/ks/
        }
    }
}
```
Where DATE must be defined as an environment variable with format yyyy-mm-dd 


##  Module 5: GBoostScore

This module builds one table with 6 partitions, one for each config file: the table contain the prediction for the nexts 3 months, that indicates if a customer is goin to cancelled or not his TDC product..
This module is going to be excute 6 times, one for each config file, that containt the info of one corresponding cluster, and the out is going to be only one table, bue with 6 partitions.
```
sparkutils-submit worker.py tests_resources/config_files/05_GBoost/params_local_gboost_score_efi.conf
sparkutils-submit worker.py tests_resources/config_files/05_GBoost/params_local_gboost_score_msi.conf
sparkutils-submit worker.py tests_resources/config_files/05_GBoost/params_local_gboost_score_neutro.conf
sparkutils-submit worker.py tests_resources/config_files/05_GBoost/params_local_gboost_score_premium.conf
sparkutils-submit worker.py tests_resources/config_files/05_GBoost/params_local_gboost_score_high_use.conf
sparkutils-submit worker.py tests_resources/config_files/05_GBoost/params_local_gboost_score_seminew.conf
```

The params_local_gboost_score_efi.conf file contents should have the following structure:

```{
       lkcol_attrition_tdc{
           stage_name = process_05_GBoostScore
           class_name = ControllerScoreGboost
           actual_date = ${?DATE}
           cluster = "EFI"
           csv = "YES"
   
           input{
               path_cluster = tests_resources/output/cluster_efi_df/
               path_gboost = tests_resources/output/gboost_efi/
               path_ks = tests_resources/output/ks/
           }
           output{
               path_attrition_prediction = tests_resources/output/attrition_prediction/
               path_attrition_txt = tests_resources/output/attrition_txt/
               path_attrition_csv = tests_resources/output/attrition_csv/
           }
       }
   }
```

The params_local_gboost_score_msi.conf file contents should have the following structure:

```
{
    lkcol_attrition_tdc{
        stage_name = process_05_GBoostScore
        class_name = ControllerScoreGboost
        actual_date = ${?DATE}
        cluster = "MSI"
        csv = "NO"

        input{
            path_cluster = tests_resources/output/cluster_msi_df/
            path_gboost = tests_resources/output/gboost_msi/
            path_ks = tests_resources/output/ks/
        }
        output{
            path_attrition_prediction = tests_resources/output/attrition_prediction/
            path_attrition_txt = tests_resources/output/attrition_txt/
            path_attrition_csv = tests_resources/output/attrition_csv/
        }
    }
}
```

The params_local_gboost_score_neutro.conf file contents should have the following structure:

```
{
    lkcol_attrition_tdc{
        stage_name = process_05_GBoostScore
        class_name = ControllerScoreGboost
        actual_date = ${?DATE}
        cluster = "NEUTRO"
        csv = "NO"

        input{
            path_cluster = tests_resources/output/cluster_neutral_df/
            path_gboost = tests_resources/output/gboost_neutral/
            path_ks = tests_resources/output/ks/
        }
        output{
            path_attrition_prediction = tests_resources/output/attrition_prediction/
            path_attrition_txt = tests_resources/output/attrition_txt/
            path_attrition_csv = tests_resources/output/attrition_csv/
        }
    }
}
```

The params_local_gboost_score_premium.conf file contents should have the following structure:

```
{
    lkcol_attrition_tdc{
        stage_name = process_05_GBoostScore
        class_name = ControllerScoreGboost
        actual_date = ${?DATE}
        cluster = "PREMIUM"
        csv = "NO"

        input{
            path_cluster = tests_resources/output/cluster_premium_df/
            path_gboost = tests_resources/output/gboost_premium/
            path_ks = tests_resources/output/ks/
        }
        output{
            path_attrition_prediction = tests_resources/output/attrition_prediction/
            path_attrition_txt = tests_resources/output/attrition_txt/
            path_attrition_csv = tests_resources/output/attrition_csv/
        }
    }
}
```

The params_local_gboost_score_high_use.conf file contents should have the following structure:

```
{
    lkcol_attrition_tdc{
        stage_name = process_05_GBoostScore
        class_name = ControllerScoreGboost
        actual_date = ${?DATE}
        cluster = "ALTA_UTILIZACION"
        csv = "NO"

        input{
            path_cluster = tests_resources/output/cluster_high_use_df/
            path_gboost = tests_resources/output/gboost_high_use/
            path_ks = tests_resources/output/ks/
        }
        output{
            path_attrition_prediction = tests_resources/output/attrition_prediction/
            path_attrition_txt = tests_resources/output/attrition_txt/
            path_attrition_csv = tests_resources/output/attrition_csv/
        }
    }
}
```

The params_local_gboost_score_seminew.conf file contents should have the following structure:

```{
       lkcol_attrition_tdc{
           stage_name = process_05_GBoostScore
           class_name = ControllerScoreGboost
           actual_date = ${?DATE}
           cluster = "SEMINUEVO"
           csv = "NO"
   
           input{
               path_cluster = tests_resources/output/seminew_df/
               path_gboost = tests_resources/output/gboost_seminew/
               path_ks = tests_resources/output/ks/
           }
           output{
               path_attrition_prediction = tests_resources/output/attrition_prediction/
               path_attrition_txt = tests_resources/output/attrition_txt/
               path_attrition_csv = tests_resources/output/attrition_csv/
           }
       }
   }
```
Where DATE must be defined as an environment variable with format yyyy-mm-dd 

