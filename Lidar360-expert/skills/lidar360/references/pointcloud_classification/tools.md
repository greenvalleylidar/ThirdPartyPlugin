# Point Cloud Classification Tools Registration
---

## Ground Classification
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| classify_ground_by_csf | Performs ground point classification for point clouds using the CSF (Cloth Simulation Filter) algorithm. It is sensitive to noise, so it is recommended to denoise the point cloud before classification. The source dataset will be updated | LiData | - |
| classify_ground_by_deep_learning | Utilizes deep learning methods to perform ground and non-ground point classification(Applicable in non-urban areas). The source dataset will be updated | LiData | - |
| classify_ground_by_progressive_tin_densification | Performs general-purpose ground point classification for LiDAR point clouds using progressive tin densification method. This tool is recommended as the default choice for ground point classification. It is sensitive to noise, so it is recommended to denoise the point cloud before classification. The source dataset will be updated | LiData | - |
| extract_median_ground_points | Used to extract a thinner and smoother middle layer of ground points from a relatively thick set of ground points. Requires the input data to have ground point.The source dataset will be updated | LiData | to_class, minimum_height, maximum_height |

---

## Noise and Outlier Classification
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| classify_noise_points | Classify the noise points in the point cloud.The source dataset will be updated | LiData | - |
| classify_isolated_points | Classify points in point cloud data as isolated points when the number of points within a given region falls below a specified threshold. This is typically used to identify isolated points in the air or below the ground surface.The source dataset will be updated | LiData | - |
| classify_low_points | Classify noise points that lie below the actual terrain surface into a specified target class. This can serve as a preprocessing step for progressive triangulated irregular network (TIN) ground point classification and cloth simulation filter (CSF) ground point classification. The source dataset will be updated | LiData | - |
| classify_closeby_points | Classify point cloud points that are adjacent to other classes. then update the source dataset | LiData | from_class, closeby_class, to_class |

---

## Object and Surface Classification
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| classify_buildings | Classify buildings in LiData point clouds using the selected classes and processing parameters, then update the source dataset | LiData | - |
| classify_water_points | Classify the points that meet the specified conditions in the from class as water bodies and extract the water body boundaries. The source point cloud dataset will be updated | LiData | - |
| classify_air_points | Classify air points in LiData point clouds using the selected classes and processing parameters, then update the source dataset | LiData | to_class |
| classify_below_surface_points | Classify below surface points in LiData point clouds using the selected classes and processing parameters, then update the source dataset | LiData | - |
| classify_top_surface | Reclassify points in the point cloud that represent the highest elevation at each location. This is crucial for creating accurate digital surface model (DSM).The source dataset will be updated | LiData | ground_class, roof_class, vegetation_class |
| classify_model_key_points | Decimate classified points appropriately.Usually used to extract ground points into a sparse set that keeps key terrain points while thinning flat regions.The source dataset will be updated | LiData | - |
| classify_tunnel_points | Classify tunnel point cloud using deep learning model. Points are classified into tunnel-related classes: 30-tunnel wall, 31-ventilation pipe, 32-cable, 36-debris, 37-noise | LiData | batch_size, input_data |

---

## Attribute-based Classification
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| classify_by_attribute | Reclassify a specific class in the point cloud into another class based on attribute features, then update the source dataset. Currently available attributes for classification include: absolute elevation, intensity, GPS time, scan angle, and return count. For data with unsatisfactory classification results, you can use this tool to revert all class if reclassification is required | LiData | attribute, min_value, max_value |
| classify_by_additional_attribute | Classify by additional attribute in LiData point clouds using the selected classes and processing parameters, then save or update the classified output dataset. Requires the input point cloud to already contain additional attributes and the `additional_attribute` field to exist and be non-empty; `min_value` and `max_value` are user-specified with `min_value <= max_value` | LiData | from_class, to_class, additional_attribute, min_value, max_value |
| classify_by_height_above_ground | This function classify points at specific heights on the terrain surface. It can quickly classify vegetation at different heights. The source dataset will be updated | LiData | to_class, min_height, max_height |
| classify_by_min_elevation_difference | Calculating the height difference between any given point and the lowest point within its surrounding specified search radius. If the height difference falls within the range of the minimum and maximum height differences, the point is marked as the target class. The source point cloud dataset will be updated | LiData | min_elevation_difference, max_elevation_difference, radius |
| classify_by_tree_attributes | Classify point cloud data by tree attributes. The source dataset will be updated | Input data | from_class, to_class |

---

## Region and Mask Classification
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| classify_by_region | Classify points of the initial class within the polygon into the target class. The source dataset will be updated | Input data | from_class, to_class |
| classify_by_mask | Mapping the mask's corresponding land cover categories onto the point cloud. This function automatically reads the categories from the mask image and, according to the geographic area represented by each pixel in the mask image, assigns the corresponding category to the point cloud within that geographic area. The mask image should be a classified mask file.The output file is same as the input file.The source point cloud dataset will  be updated | Input data | mask_class, target_class |

---

## Machine Learning Inference
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| classify_by_deep_learning | Classify point cloud data using a deep learning segmentation model, applicable to various scenarios including airborne urban, airborne rural, terrestrial forestry, terrestrial parks, and vehicle-mounted roadways.The source dataset will be updated | LiData | from_class |
| classify_by_machine_learning | Classify the point cloud data using random forest algorithm to obtain the classified point cloud and a machine learning model file in VCM format. The source dataset will be updated | LiData | training_class |
| classify_by_trained_ml_model | Classify the input point cloud using a trained machine learning model in VCM format.The source dataset will be updated | LiData + VCM | - |
| classify_low_and_high_vegetation | Classify low and high vegetation from TLS forest point cloud data using a deep learning segmentation model.The source dataset will be updated | LiData | from_class |
| classify_using_trained_pano_image_tree_classification_model | Classify tree species from panoramic images using a trained pano image tree classification model. Each image is classified and results are written to a three-column CSV: ImageFile, TreeSpecies, and Confidence | Panoramic images directory | model, input_data |

---

## Model Training
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| train_point_cloud_classification_model | Train a deep learning model for point cloud classification. Supports multiple network architectures including DRINet, SPVNAS, PVCNN, KPConv, and MinkUNet. Configure model parameters, training settings, data transforms, and split functions | Input data | task_name, task_description, model, training, split_transform |
| train_image_classification_model | Train a deep learning model for image classification. Supports segmentation and detection tasks. Configure model parameters, training settings, and data transforms | Input data | task_name, model_list, class_conversion_setting, training |
| train_pano_image_tree_classification_model | Train a deep learning model to classify tree species directly from panoramic images. Provide panoramic image data together with the corresponding tree-species label files (CSV with image-name and species columns) | Panoramic images + CSV labels | task_name, model_list, training, input_data |

---

## Road Extraction
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| extract_roads_by_deep_learning | Extracting road polygons using a deep learning model, generating road line vector files and corresponding road mask images. The mask images contain two classification values: class value 0 indicates unclassified, while class value 1 indicates roads | TIF/TIFF/JPG/BMP | - |

---

## Common Parameter Explanation

### Classification Method Types
| Method | Description | Best For |
|---|------|---------|
| CSF | Cloth Simulation Filter ground classification; sensitive to noise | Simple terrain after noise removal |
| Triangulation | Iterative TIN ground classification | Complex terrain after noise removal |
| Deep Learning | Built-in or trained neural network classification | Urban, rural, forestry, park, and road scenes |
| Random Forest | VCM model based machine learning classification | Classifying with selected training classes and object features |

### Common Classification Classes
| Class ID | Class Name | Description |
|---|------|---------|
| 0 | Never classified | Unclassified points |
| 1 | Unclassified | Default unclassified |
| 2 | Ground | Ground surface |
| 3 | Low Vegetation | Grass, bushes |
| 4 | Medium Vegetation | Trees, shrubs |
| 5 | High Vegetation | Tall trees |
| 6 | Building | Building structures |
| 9 | Water | Water bodies |
| 17 | Bridge | Bridge structures |
| 64 | Reserved | Reserved for future use |

---

Detailed parameters: {SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "pointcloud_classification-toolID"
