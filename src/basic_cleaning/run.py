#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(project="nyc_airbnb", group="basic_cleaning", job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    logger.info("Downloading artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    # Create a pandas data frame from this artificact
    df = pd.read_csv(artifact_local_path)

    logger.info("Cleaning Data")
    # Select rows with appropriate price
    idx = df['price'].between(args.min_price, args.max_price)
    # Create a dataframe with just those rows
    df = df[idx].copy()
    # Convert last_review Dtype from string to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info("Saving Results")
    df.to_csv("clean_sample.csv", index=False)

    logger.info("Uploading Cleaned Data to W&B")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="input name of data file",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Output file name of cleaned data file",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of data produced",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of the output data",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="minimum price to consider for an airbnb",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="minimum price to consider for an airbnb",
        required=True
    )


    args = parser.parse_args()

    go(args)
