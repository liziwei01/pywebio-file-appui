'''
Author: liziwei01
Date: 2022-07-10 16:46:34
LastEditors: liziwei01
LastEditTime: 2022-07-10 16:47:47
Description: file content
'''
from abc import abstractmethod, ABCMeta
# The error built-in interface type is the conventional interface for
# representing an error condition, with the None value representing no error.
class error(metaclass=ABCMeta):
	@abstractmethod
	def Error() -> str:
		'''
		Return the error message.
		'''
		...