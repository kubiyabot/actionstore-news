# Custom actions examples
This repository contains an example actions which can be run in within the Kubiya platform as part of workflows

# How to upload it to Kubiya

The Kubiya platform can execute any type of Python code in a serverless way.  The reason why you would want to upload such actions to Kubiya is mainly in order to use those inside **workflows**

### Perquisites
* You'll need the Kubiya command line utility installed on your computer *

## Step 1: Bundle the Python solution as an action store

1. Clone this repository to your local file system:
`git clone https://github.com/kubiyabot/actionstore-news`
The cloned repository has two files in it:
	* media.py
		A simple python snippet with some functions which are used to get news from different internet sources
	* requirements.txt
	A standard Python pip requirements file which contains the relevant runtime dependencies media.py requires - just as any Python program
2. Bundle the cloned repository as an action store using the CLI:
`kubiya action-store bundle --language python --store-name get_the_news .`
Where:
* --runtime flag stands for *runtime* which in our case is *python*
* --name flag stands for the action store *name* which is *get_the_news*
* . (last flag) stands for the current working directory files, which contains the `media.py` and the `requirements.txt` file

It might take a few seconds for the bundling to complete, on success you should see similar indication on your terminal:
 `{"name":"get_the_news","url":"<repo>:adcb1b54-c9b3-4b04-8f00-82d3170de726","metadata":{"kubiya_version":"python-sdk: 0.0.17","name":"actionstore","registered_actions":["get_all_sources","get_article","get_articles","get_url_for_media"],"secrets":[],"version":"bundled at: 2022-11-11 15:03:17.729797"}}`

3. Check that the defined Python functions inside `media.py` are discovered properly using the `kubiya action-store describe` CLI command:

`kubiya action-store describe get_the_news`
Where:
* get_the_news (last flag) is the action store we want to describe

You should see the following output in your terminal:

`action store name is: [get_the_news]
url is: <repo>:adcb1b54-c9b3-4b04-8f00-82d3170de726
actions
get_all_sources
get_article
get_articles
get_url_for_media`

You should see all of the actions which are part of the media.py Python snippet.

## Step 2: Run actions which are defined as part of the action-store

1. Let's try to execute the `get_all_sources` function to make sure that our action store works as expected:
`kubiya action execute --action-name get_all_sources --store-name get_the_news -j {}`

Where: 
- --action-name flag stands for the `action` name 
- --store-name stands for the `action-store` name
- -j stands for json input which could be used to pass parameters to the action call (in the example below the parameters are empty)

You should see the following output:
`{"input":{},"output":["bbc","cnn","abc news","cbs news","fox news","new york times","nbc","washington post","usa today"],"error":null}`

## Using bundled actions inside workflows
Given example workflow step:
```
- id: get_the_news
	type: action
	action:
		store: get_the_news
		name: get_all_sources
		parameters: {}
```
This step will store a variable called `news_sources` to the workflow variables context, this step output can now be used as part of other steps to show prompts, etc

Full example:
```
- id: news_sources
	type: action
	action:
		store: get_the_news
		name: get_all_sources
		parameters: {}
  - id: multi
    type: multi_input
    prompt: "Need some help here"
    inputs:
      - id: selected_news
        type: input
        value_type: enum
        prompt: "Which news would you like to watch?"
        possible_values: ${news_sources}
  - id: send_information
    type: message
    prompt: |
      You just selected `${selected_news}`
```

The example below does the following:
1) Executes the `get_all_sources` action from the `get_the_news` action store
2) Stores the output as a variable called: `news_sources` - which is the step name
3) Pops a modal with a simple question - which news to watch - where the available options are the fetched sources
4) As soon as the modal is filled, a message will be sent with the selected source
