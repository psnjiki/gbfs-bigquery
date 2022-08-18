## <span style="color:blue">**COLLECT BIKESHARE FEEDS ON BIGQQUERY**</span>
---
Many bikeshare operators publish real time data on stations status and bikes availability.

This job collects current status of bikeshare stations and bikes of a given operator.

Such data is usually accessible via url links to multiple json data.

The data is timed and stored to a user provided bigquery dataset.

The job is containerized and can be deployed to the cloud and scheduled to run frequently (ex. every minute).

The resulting output can help analyze and model stations status and bike availabilty dynamics.

To run the job, the user must set a few parameters in the file params.json 
or provide corresponding environment variables when running the image.
That includes: the base url to json feeds, the name of the bigquery 
dataset to serve as destination and the feeds language.

To test the job with docker in local, run the file test.sh from the project directory.

[Bikeshare operators](https://github.com/NABSA/gbfs/blob/master/systems.csv)

[gbfs feeds specification](https://github.com/NABSA/gbfs)

[ex. gbfs feeds](https://gbfs.velobixi.com/gbfs/gbfs.json)

[build a docker image in the cloud](https://cloud.google.com/build/docs/build-push-docker-image)
