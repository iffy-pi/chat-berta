## Current Layout

First, a quick overview of the current layout of the application:

![[Pasted image 20230126005727.png]]

The labelled items above are the React components used in the source code. Each of these components is wrapped with a `div` container with the class name `basic-container`, and that is what generates the simple black borders on the side.

The message components with thicker lines are summarizer messages. (That is, messages included in the summary paragraph)

The OptionsToggle will be implemented as a checkbox component, in a few days but as for now it is just implemented as two buttons. (The CSS can design it as a checkbox).

We also have different components for different states of the `SummaryView` content.

When a request has not been made, the `SummaryContentUnset` component is in use:

![[Pasted image 20230125232814.png]]

When a request is made and is loading, we use the `SummaryContentLoading` component:

![[Pasted image 20230125232901.png]]

We also have an error component `SummaryContentError` that is rendered if the summary request fails for some reason:

![[Pasted image 20230125232946.png]]

The idea with this frontend CSS design is that you can simply make the CSS classes to implement the frontend design we desire for each component. I can then use those class names in the React source code to implement the different required items.

## Desired Design
The following diagram outlines the required design, highlighting the different components in the pretty version:

### Main View
The main view will look something similar to this, I have labelled the required components in the below picture.

![[Pasted image 20230126005750.png]]

### Phone Layout
On a phone, the SummaryView component should automatically fall under the ControlBoard component (most likely implemented with CSS Flex):

![[Pasted image 20230126004739.png]]

### Initial Page
The Initial page should have some basic info on the SummaryView component such as:

![[Pasted image 20230126004839.png]]

We also have the different layouts for the different input options, the above is for uploading a file, the below is for putting a transcript:

![[Pasted image 20230126004915.png]]

### Loading Page
The loading page will have a simple loading gif (not rendered below):

![[Pasted image 20230126005005.png]]

### Error Page
If the summary request failed, we can have a simple error page that returns the error information:

![[Pasted image 20230126005034.png]]



