Micro task repository for chaoss gsoc project : Reporting of CHAOSS Metrics



**Microtask 1**: Produce a listing of the number of new committers per month, and the number of commits for each of them, as a table and as a CSV file. Use the GrimoireLab enriched index for git.

**Microtask 2**: Produce a chart showing the distribution of time-to-close (using the corresponding field in the GrimoireLab enriched index for GitHub issues) for issues already closed, and opened during the last six months.

**Microtask 3**: Produce a listing of repositories, as a table and as CSV file, with the number of commits authored, issues opened, and pull requests opened, during the last three months, ordered by the total number (commits plus issues plus pull requests).


**Note**:

1.Elastic Search is required to run task 1 and task 2.

2.Make sure you have perceval python module to run task 3,if not you can install it using

```
pip3 install perceval
```

If you are stuck somewhere feel free to contact me.
If you want to suggest something ,feel free to open a pull request.

For downloading requirements and tutorials visit [tutorial](https://grimoirelab.gitbooks.io/tutorial/content/)
