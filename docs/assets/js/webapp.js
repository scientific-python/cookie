const DEFAULT_MSG =
  "Enter a GitHub repo and branch to review. Runs Python entirely in your browser using WebAssembly. Built with React, MaterialUI, and Pyodide.";

const urlParams = new URLSearchParams(window.location.search);
const baseurl = window.location.pathname;

function Heading(props) {
  return (
    <MaterialUI.Box sx={{ flexGrow: 1, mb: 2 }}>
      <MaterialUI.AppBar position="static">
        <MaterialUI.Toolbar>
          <MaterialUI.Typography
            variant="h6"
            component="div"
            sx={{ flexGrow: 1 }}
          >
            Repo-Review
          </MaterialUI.Typography>
          <MaterialUI.Button
            href="https://github.com/scientific-python/repo-review"
            color="inherit"
          >
            Source
          </MaterialUI.Button>
        </MaterialUI.Toolbar>
      </MaterialUI.AppBar>
    </MaterialUI.Box>
  );
}

function IfUrlLink({ name, url, color }) {
  if (url) {
    return (
      <MaterialUI.Typography
        sx={{ display: "inline" }}
        component="span"
        variant="body2"
        color={color}
        component="a"
        href={url}
        target="_blank"
      >
        {name}
      </MaterialUI.Typography>
    );
  }
  return (
    <MaterialUI.Typography
      sx={{ display: "inline" }}
      component="span"
      variant="body2"
      color={color}
    >
      {name}
    </MaterialUI.Typography>
  );
}

function Results(props) {
  const output = [];
  for (const key in props.results) {
    const inner_results = props.results[key];
    const results_components = inner_results.map((result) => {
      const text_color =
        result.state === false
          ? "error.main"
          : result.state === true
          ? "text.primary"
          : "info.main";
      const details =
        result.state === false ? (
          <span dangerouslySetInnerHTML={{ __html: result.err_msg }} />
        ) : null;
      const color =
        result.state === false
          ? "error"
          : result.state === true
          ? "success"
          : "info";
      const icon = (
        <MaterialUI.Icon color={color}>
          {result.state === false
            ? "report"
            : result.state === true
            ? "check_box"
            : "info"}
        </MaterialUI.Icon>
      );

      const skipped = (
        <MaterialUI.Typography
          sx={{ display: "inline" }}
          component="span"
          variant="body2"
          color="text.disabled"
        >
          {" [skipped]"}
        </MaterialUI.Typography>
      );
      const msg = (
        <React.Fragment>
          <IfUrlLink name={result.name} url={result.url} color={text_color} />
          <IfUrlLink name={": "} url={""} color={text_color} />
          <React.Fragment>
            <MaterialUI.Typography
              sx={{ display: "inline" }}
              component="span"
              color={text_color}
            >
              {result.description}
            </MaterialUI.Typography>
          </React.Fragment>
          {result.state === undefined && skipped}
        </React.Fragment>
      );
      return (
        <MaterialUI.ListItem disablePadding key={result.name}>
          <MaterialUI.ListItemIcon>{icon}</MaterialUI.ListItemIcon>
          <MaterialUI.ListItemText
            primary={msg}
            secondary={details}
            href={result.url}
          />
        </MaterialUI.ListItem>
      );
    });

    output.push(
      <li key={`section-${key}`}>
        <ul>
          <MaterialUI.ListSubheader>
            {props.families[key]}
          </MaterialUI.ListSubheader>
          {results_components}
        </ul>
      </li>,
    );
  }

  return (
    <MaterialUI.Box sx={{ bgcolor: "background.paper" }}>
      <MaterialUI.List subheader={<li />} overflow="auto">
        {output}
      </MaterialUI.List>
    </MaterialUI.Box>
  );
}

async function prepare_pyodide(deps) {
  const deps_str = deps.map((i) => `"${i}"`).join(", ");
  const pyodide = await loadPyodide();

  await pyodide.loadPackage("micropip");
  await pyodide.runPythonAsync(`
        import micropip
        await micropip.install([${deps_str}])
    `);
  return pyodide;
}

function MyThemeProvider(props) {
  const prefersDarkMode = MaterialUI.useMediaQuery(
    "(prefers-color-scheme: dark)",
  );

  const theme = React.useMemo(
    () =>
      MaterialUI.createTheme({
        palette: {
          mode: prefersDarkMode ? "dark" : "light",
        },
      }),
    [prefersDarkMode],
  );

  return (
    <MaterialUI.ThemeProvider theme={theme}>
      {props.children}
    </MaterialUI.ThemeProvider>
  );
}

class App extends React.Component {
  constructor(props) {
    super(props);
    const deps_str = props.deps.join(" ");
    this.state = {
      results: [],
      repo: urlParams.get("repo") || "",
      branch: urlParams.get("branch") || "",
      msg: `${DEFAULT_MSG} Packages: ${deps_str}`,
      progress: false,
      err_msg: "",
      url: "",
    };
    this.pyodide_promise = prepare_pyodide(props.deps);
  }

  handleCompute() {
    if (!this.state.repo || !this.state.branch) {
      this.setState({ results: [], msg: DEFAULT_MSG });
      window.history.replaceState(null, "", baseurl);
      alert(
        `Please enter a repo (${this.state.repo}) and branch (${this.state.branch})`,
      );
      return;
    }
    const local_params = new URLSearchParams({
      repo: this.state.repo,
      branch: this.state.branch,
    });
    window.history.replaceState(null, "", `${baseurl}?${local_params}`);
    this.setState({
      results: [],
      msg: "Running Python via Pyodide",
      progress: true,
    });
    const state = this.state;
    this.pyodide_promise.then((pyodide) => {
      var families_checks;
      try {
        families_checks = pyodide.runPython(`
            from pyodide.http import open_url
            from repo_review.processor import process
            from repo_review.ghpath import GHPath

            GHPath.open_url = staticmethod(open_url)

            package = GHPath(repo="${state.repo}", branch="${state.branch}")
            process(package)
        `);
      } catch (e) {
        if (e.message.includes("KeyError: 'tree'")) {
          this.setState({
            msg: DEFAULT_MSG,
            progress: false,
            err_msg: "Invalid repository or branch. Please try again.",
          });
          return;
        }
        this.setState({
          progress: false,
          err_msg: e.message,
        });
        return;
      }

      const families_dict = families_checks.get(0);
      const results_list = families_checks.get(1);

      const results = {};
      const families = {};
      for (const val of families_dict) {
        results[val] = [];
        families[val] = families_dict.get(val).get("name");
      }
      console.log(families);
      for (const val of results_list) {
        results[val.family].push({
          name: val.name.toString(),
          description: val.description.toString(),
          state: val.result,
          err_msg: val.err_as_html().toString(),
          url: val.url.toString(),
        });
      }

      this.setState({
        results: results,
        families: families,
        msg: `Results for ${state.repo}@${state.branch}`,
        progress: false,
        err_msg: "",
        url: "",
      });

      results_list.destroy();
      families_dict.destroy();
    });
  }

  componentDidMount() {
    if (urlParams.get("repo") && urlParams.get("branch")) {
      this.handleCompute();
    }
  }

  render() {
    const common_branches = ["main", "master", "develop", "stable"];
    return (
      <MyThemeProvider>
        <MaterialUI.CssBaseline />
        <MaterialUI.Box>
          {this.props.header && <Heading />}
          <MaterialUI.Stack
            direction="row"
            spacing={2}
            alignItems="top"
            sx={{ m: 1, mb: 3 }}
          >
            <MaterialUI.TextField
              id="repo-select"
              label="Org/Repo"
              helperText="e.g. scikit-hep/hist"
              variant="outlined"
              autoFocus={true}
              onInput={(e) => this.setState({ repo: e.target.value })}
              defaultValue={urlParams.get("repo")}
              sx={{ flexGrow: 3 }}
            />
            <MaterialUI.Autocomplete
              disablePortal
              id="branch-select"
              options={common_branches}
              freeSolo={true}
              onInputChange={(e, value) => this.setState({ branch: value })}
              defaultValue={urlParams.get("branch")}
              renderInput={(params) => (
                <MaterialUI.TextField
                  {...params}
                  label="Branch"
                  variant="outlined"
                  helperText="e.g. main"
                  sx={{ flexGrow: 2, minWidth: 130 }}
                />
              )}
            />

            <MaterialUI.Button
              onClick={() => this.handleCompute()}
              variant="contained"
              size="large"
              disabled={
                this.state.progress || !this.state.repo || !this.state.branch
              }
            >
              <MaterialUI.Icon>start</MaterialUI.Icon>
            </MaterialUI.Button>
          </MaterialUI.Stack>
          <MaterialUI.Paper elevation={3}>
            <MaterialUI.Box sx={{ p: 2 }}>
              <MaterialUI.Typography variant="body1" component="div">
                {this.state.msg}
              </MaterialUI.Typography>
              {this.state.progress && <MaterialUI.LinearProgress />}
              {this.state.err_msg && (
                <MaterialUI.Typography
                  variant="body1"
                  component="div"
                  color="error"
                >
                  {" "}
                  {this.state.err_msg}{" "}
                </MaterialUI.Typography>
              )}
            </MaterialUI.Box>
            <Results
              results={this.state.results}
              families={this.state.families}
            />
          </MaterialUI.Paper>
        </MaterialUI.Box>
      </MyThemeProvider>
    );
  }
}
