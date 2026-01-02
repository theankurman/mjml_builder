# MJML Builder

This project is a python library used to build mjml markup in a programmatic way.

## Table of contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [How to use](#how-to-use)
  - [Building the email](#building-the-email)
    - [Using the builder](#using-the-builder)
    - [Using components directly](#using-components-directly)
  - [Generating markup](#generating-markup)
    - [Generate mjml markup](#generate-mjml-markup)
    - [Generate html markup](#generate-html-markup)
    - [Generate text](#generate-text)
    - [Generate dict](#generate-dict)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## How to use

### Building the email

There are two ways to build an email. The two examples below both result in the same output.

#### Using the builder

```python
from mjml_builder import components as c
from mjml_builder import Builder

email_builder = (
    Builder()
    .add_content("Hello", font_size="20px", align="center")
    .add_column()
    .add_content("World", color="red")
    .add_section()
    .add_content(
        c.Accordion(
            c.AccordionElement("Title 1", "Content of the accordion 1"),
            c.AccordionElement("Title 2", "Content of the accordion 1"),
        )
    )
    .add_section()
    .add_content(c.Image("https://picsum.photos/200", width="200px"))
)
email = email_builder.build()
```

#### Using components directly

```python
from mjml_builder import components as c

email = c.Body(
    c.Section(
        c.Column(
            c.Text(
                "Hello",
                align="center",
                font_size="20px",
            )
        ),
        c.Column(
            c.Text(
                "World",
                color="red",
            )
        ),
    ),
    c.Section(
        c.Column(
            c.Accordion(
                c.AccordionElement("Title 1", "Content of the accordion 1"),
                c.AccordionElement("Title 2", "Content of the accordion 1"),
            )
        )
    ),
    c.Section(c.Column(
        c.Image("https://picsum.photos/200", width="200px")
    )),
)
```

### Generating markup

The email component built using the `Builder().build()` or using the components directly has properties that can be used to access various representations of the email.

#### Generate mjml markup

You can generate a mjml representation of the email using.

```python
email.mjml
```

#### Generate html markup

You can generate a html representation of the email using.

```python
email.html
```

To generate html **one** of the following must be true.

- Have the `mrml` library installed using

  ```bash
  uv add mrml # or pip install mrml
  ```

- Have the `mjml` cli available in path. This can be installed using

  ```bash
  npm i -g mjml # or bun,pnpm etc
  ```

- Have one of `bun`, `pnpm` or `npm` installed. The html will then be generated using `bunx mjml`, `pnpx mjml` or `npx mjml`.

#### Generate text

You can generate a text representation of the email using.

```python
email.text
```

#### Generate dict

You can generate a dict representation of the email using.
This dict matches the format defined in the [MJML Docs](https://documentation.mjml.io/#using-mjml-in-json)
