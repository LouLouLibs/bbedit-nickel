# Open this file in BBEdit: the language should be Nickel.
let greet = fun name => "Hello, %{name}!" in
{
  name | String | default = "Nickel",
  enabled | Bool = true,
  port | Number | doc "The listening port" = 8080,
  message = greet name,
  tags = ['Development, 'Production],
  nested = { values = [1, 2, 3], nothing = null },
  multiline = m%"
    Quotes "inside" and # characters remain part of the string.
    Hello, %{name}!
  "% ,
  extra_delimiters = m%%"
    A literal "% does not end this string.
  "%%,
}
