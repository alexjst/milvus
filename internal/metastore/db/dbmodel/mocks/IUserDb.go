// Code generated by mockery v2.14.0. DO NOT EDIT.

package mocks

import (
	dbmodel "github.com/milvus-io/milvus/internal/metastore/db/dbmodel"
	mock "github.com/stretchr/testify/mock"
)

// IUserDb is an autogenerated mock type for the IUserDb type
type IUserDb struct {
	mock.Mock
}

// GetByUsername provides a mock function with given fields: tenantID, username
func (_m *IUserDb) GetByUsername(tenantID string, username string) (*dbmodel.User, error) {
	ret := _m.Called(tenantID, username)

	var r0 *dbmodel.User
	if rf, ok := ret.Get(0).(func(string, string) *dbmodel.User); ok {
		r0 = rf(tenantID, username)
	} else {
		if ret.Get(0) != nil {
			r0 = ret.Get(0).(*dbmodel.User)
		}
	}

	var r1 error
	if rf, ok := ret.Get(1).(func(string, string) error); ok {
		r1 = rf(tenantID, username)
	} else {
		r1 = ret.Error(1)
	}

	return r0, r1
}

// Insert provides a mock function with given fields: in
func (_m *IUserDb) Insert(in *dbmodel.User) error {
	ret := _m.Called(in)

	var r0 error
	if rf, ok := ret.Get(0).(func(*dbmodel.User) error); ok {
		r0 = rf(in)
	} else {
		r0 = ret.Error(0)
	}

	return r0
}

// ListUsername provides a mock function with given fields: tenantID
func (_m *IUserDb) ListUsername(tenantID string) ([]string, error) {
	ret := _m.Called(tenantID)

	var r0 []string
	if rf, ok := ret.Get(0).(func(string) []string); ok {
		r0 = rf(tenantID)
	} else {
		if ret.Get(0) != nil {
			r0 = ret.Get(0).([]string)
		}
	}

	var r1 error
	if rf, ok := ret.Get(1).(func(string) error); ok {
		r1 = rf(tenantID)
	} else {
		r1 = ret.Error(1)
	}

	return r0, r1
}

// MarkDeletedByUsername provides a mock function with given fields: tenantID, username
func (_m *IUserDb) MarkDeletedByUsername(tenantID string, username string) error {
	ret := _m.Called(tenantID, username)

	var r0 error
	if rf, ok := ret.Get(0).(func(string, string) error); ok {
		r0 = rf(tenantID, username)
	} else {
		r0 = ret.Error(0)
	}

	return r0
}

type mockConstructorTestingTNewIUserDb interface {
	mock.TestingT
	Cleanup(func())
}

// NewIUserDb creates a new instance of IUserDb. It also registers a testing interface on the mock and a cleanup function to assert the mocks expectations.
func NewIUserDb(t mockConstructorTestingTNewIUserDb) *IUserDb {
	mock := &IUserDb{}
	mock.Mock.Test(t)

	t.Cleanup(func() { mock.AssertExpectations(t) })

	return mock
}
