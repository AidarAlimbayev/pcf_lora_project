import fiftyone as fo
import fiftyone.zoo as foz

# dataset = foz.load_zoo_dataset('quickstart')
# session = fo.launch_app(dataset)


# dataset = foz.load_zoo_dataset(
#     "open-images-v6",
#     split="validation",
#     max_samples=100,
#     seed=51,
#     shuffle=True,
# )


cattle_subset = foz.load_zoo_dataset(
    "open-images-v6",
    split="validation",
    label_types=["detections", "classifications"],
    classes=["Cattle"],
    max_samples=250,
    seed=51,
    shuffle=True,
    dataset_name="cattle-subset",
)

session = fo.launch_app(cattle_subset)

session.wait()