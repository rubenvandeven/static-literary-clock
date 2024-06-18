# Static Literary Clock

Basic python server with no dependencies. It produces a webpage without javascript, so that old e-readers can render the page.

Note that, because the page cannot use javascript, it uses the server's clock. So it should be run from e.g. your homeserver.

To avoid duplication of work, the code relies on the collection of quotes [maintained by Johannes Enevoldsen](https://github.com/JohannesNE/literature-clock).
The original idea and data proccessing was done by [Jaap Meijers](https://www.instructables.com/Literary-Clock-Made-From-E-reader/).
The collection of quotes what originally gathered by the Guardian ([here](https://www.theguardian.com/books/table/2011/apr/21/literary-clock?CMP=twt_gu) and [here](https://www.guardian.co.uk/books/booksblog/2011/apr/15/christian-marclay-the-clock-literature))

## Usage

Make sure you have Python 3. As it has no dependencies outside of the standard lib, just run:

```bash
python server.py
```