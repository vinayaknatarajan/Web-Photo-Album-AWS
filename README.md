## WebPhotoAlbum

### PhotoSearchFrontend
Files including API Gateway Client and other HTML, CSS, JS files are in this directory.

### Index directory
Contains Lambda function for the first Lambda which is invoked on upload of a file in S3 bucket.
Does the work of indexing images, that is, uses Rekognition to get tags form the image and creates an index in ElasticSearch.

### Search directory
Does the work of getting tags from the input request using Lex Bot and then finding images with those tags and returning images array.

### CD Pipeline using AWS CodePipeline(YAML files)
Creates 2 lambda functions with VPC configuration and having their permissions attached as predefined roles.
Execution done using AWS Code Pipeline.
