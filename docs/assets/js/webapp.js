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
            Scikit-HEP-Repo-Review
          </MaterialUI.Typography>
          <MaterialUI.Button
            href="https://scikit-hep.org/developer"
            color="inherit"
          >
            Developer Guidelines
          </MaterialUI.Button>
          <MaterialUI.Button
            href="https://github.com/scikit-hep/repo-review"
            color="inherit"
          >
            Source
          </MaterialUI.Button>
        </MaterialUI.Toolbar>
      </MaterialUI.AppBar>
    </MaterialUI.Box>
  );
}

function Results(props) {
  const output = [];
  for (const key in props.results) {
    const inner_results = props.results[key];
    const results_components = inner_results.map((result) => {
      const details =
        result.state === false ? (
          <span dangerouslySetInnerHTML={{ __html: result.err_msg }} />
        ) : null;
      const color =
        result.state === false
          ? "error"
          : result.state === true
          ? "success"
          : "warning";
      const icon = (
        <MaterialUI.Icon color={color}>
          {result.state === false
            ? "error"
            : result.state === true
            ? "check_circle"
            : "warning"}
        </MaterialUI.Icon>
      );
      const skipped = (
        <MaterialUI.Typography
          sx={{ display: "inline" }}
          component="span"
          variant="body2"
        >
          {" [skipped]"}
        </MaterialUI.Typography>
      );
      const msg = (
        <React.Fragment>
          <MaterialUI.Typography
            sx={{ display: "inline" }}
            component="span"
            variant="body2"
            color="text.primary"
          >
            {result.name + ": "}
          </MaterialUI.Typography>
          <React.Fragment>{result.description}</React.Fragment>
          {result.state === undefined && skipped}
        </React.Fragment>
      );
      return (
        <MaterialUI.ListItem disablePadding key={result.name}>
          <MaterialUI.ListItemIcon>{icon}</MaterialUI.ListItemIcon>
          <MaterialUI.ListItemText primary={msg} secondary={details} />
        </MaterialUI.ListItem>
      );
    });

    output.push(
      <li key={`section-${key}`}>
        <ul>
          <MaterialUI.ListSubheader>{key}</MaterialUI.ListSubheader>
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

async function prepare_pyodide() {
  const pyodide = await loadPyodide();

  await pyodide.loadPackage("micropip");
  await pyodide.runPythonAsync(`
        import micropip
        await micropip.install(["scikit_hep_repo_review==0.5.0"])
    `);
  return pyodide;
}

const pyodide_promise = prepare_pyodide();

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
    this.state = {
      results: [],
      repo: urlParams.get("repo") || "",
      branch: urlParams.get("branch") || "",
      msg: DEFAULT_MSG,
      progress: false,
      err_msg: "",
    };
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
    pyodide_promise.then((pyodide) => {
      var results_dict;
      try {
        results_dict = pyodide.runPython(`
                    from pyodide.http import open_url
                    from scikit_hep_repo_review.processor import process
                    from scikit_hep_repo_review.ghpath import GHPath

                    GHPath.open_url = staticmethod(open_url)

                    package = GHPath(repo="${state.repo}", branch="${state.branch}")
                    results_dict = process(package)
                    results_dict
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

      const results = {};
      for (const res of results_dict) {
        const vals = results_dict.get(res);
        const inner_results = [];
        for (const val of vals) {
          inner_results.push({
            name: val.name.toString(),
            description: val.description.toString(),
            state: val.result,
            err_msg: val.err_markdown().toString(),
          });
        }
        results[res] = inner_results;
      }

      this.setState({
        results: results,
        msg: `Results for ${state.repo}@${state.branch}`,
        progress: false,
        err_msg: "",
      });
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
            <Results results={this.state.results} />
          </MaterialUI.Paper>
        </MaterialUI.Box>
      </MyThemeProvider>
    );
  }
}
