%
%  Auto-generated file, do not modify.
%  Instead, copy this file to the man/ folder, remove this warning, and edit freely.
%  Use Git to identify changes in this file which suggest where to change your edited copy.
%
\name{SubmissionViewSchema}
\alias{SubmissionViewSchema}
\docType{methods}
\title{
Constructor for objects of type SubmissionViewSchema
}
\description{
A SubmissionViewSchema is a Entity that displays all files/projects
(depending on user choice) within a given set of scopes
}
\usage{
SubmissionViewSchema(name=NULL, columns=NULL, parent=NULL, scopes=NULL, addDefaultViewColumns=TRUE, addAnnotationColumns=TRUE, ignoredAnnotationColumnNames=list(), properties=NULL, annotations=NULL, local_state=NULL)
}
\arguments{
\item{name}{                            the name of the Entity View Table object\cr
}
\item{columns}{                         a list of Column objects or their IDs. These are optional.\cr
}
\item{parent}{                          the project in Synapse to which this table belongs\cr
}
\item{scopes}{                          a list of Evaluation Queues or their ids\cr
}
\item{addDefaultViewColumns}{           If true, adds all default columns (e.g. name, createdOn, modifiedBy etc.)\cr
                                        Defaults to True.\cr
                                        The default columns will be added after a call to\cr
                                        synapseclient.Synapse.store.\cr
}
\item{addAnnotationColumns}{            If true, adds columns for all annotation keys defined across all Entities in\cr
                                        the SubmissionViewSchema's scope. Defaults to True.\cr
                                        The annotation columns will be added after a call to\cr
                                        synapseclient.Synapse.store.\cr
}
\item{ignoredAnnotationColumnNames}{    A list of strings representing annotation names.\cr
                                        When addAnnotationColumns is True, the names in this list will not be\cr
                                        automatically added as columns to the SubmissionViewSchema if they exist in\cr
                                        any of the defined scopes.\cr
}
\item{properties}{                      A map of Synapse properties\cr
}
\item{annotations}{                     A map of user defined annotations\cr
}
\item{local_state}{                     Internal use only}
}
\details{
% A detailed if possible precise description of the functionality provided, extending the basic information in the \description slot.
}
\value{
An object of type SubmissionViewSchema
}
\references{
% A section with references to the literature. Use \url{} or \href{}{} for web pointers.
}
\note{
% Use this for a special note you want to have pointed out. 
}
\seealso{
% Pointers to related R objects, using \code{\link{...}} to refer to them.
}
% Examples of how to use the function. 
% Examples are not only useful for documentation purposes, but also provide test code used for diagnostic checking of R code. 
% By default, text will be displayed in the output of the help page and run by example() and by R CMD check. 
% You can use \dontrun{} for text that should only be shown, but not run, and \dontshow{} for extra commands 
% for testing that should not be shown to users, but will be run by example(). 
\examples{

}



